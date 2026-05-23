from datetime import datetime
from templates import (
    correo_agradecimiento_backup,
    get_reminder_email,
    get_preregistro_backup_email,
)
from mail.mailer import send_email
import asyncio
import os
import redis
import logging
from config.form_routes import (
    load_form_routes,
    resolve_cc,
)

logger = logging.getLogger(__name__)

_, _PROJECT_CONFIGS = load_form_routes()

def get_redis_client():
    """Función local para obtener cliente Redis"""
    return redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6380)),
        decode_responses=True,
        db=0
    )

################# Envío de correos de recordatorios ##################

def _as_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _get_project_context(participante, project_configs):
    project_id = participante.get("project_id")
    project_config = project_configs.get(str(project_id), {})
    project_name = participante.get("project_name") or project_config.get("project_name") or "Proyecto"
    reminder_enabled = _as_bool(participante.get("reminder_enabled"), default=False)
    reminder_url = (participante.get("reminder_url") or "").strip()
    return project_id, project_name, reminder_enabled, reminder_url


async def enviar_recordatorio_individual(participante, redis_client, semaphore, project_configs):
    async with semaphore:
        try:
            ultimo_recordatorio_key = f"recordatorio:ultimo:{participante['participante_id']}"
            ahora = int(datetime.now().timestamp())
            
            # Solo se crea si no existe
            if redis_client.set(ultimo_recordatorio_key, str(ahora), nx=True, ex=518400):  # 6 días
                # La clave se crea y envia recordatorio
                project_id, project_name, reminder_enabled, reminder_url = _get_project_context(participante, project_configs)
                if not reminder_enabled or not reminder_url:
                    # No debería ocurrir porque ya se filtran participantes sin reminder activo por ruta.
                    return 0
                payload = dict(participante)
                payload["project_name"] = project_name
                payload["reminder_url"] = reminder_url
                try:
                    subject, message = get_reminder_email(payload, project_id=project_id)
                except ValueError as e:
                    logger.error(
                        "Error de plantilla de recordatorio project_id=%s participant_id=%s error=%s",
                        project_id,
                        participante["participante_id"],
                        str(e),
                    )
                    return 0
                cc_recipients = resolve_cc(project_config=project_configs.get(str(project_id), {}))
                await send_email(
                    subject=subject,
                    html_message=message,
                    recipient=participante["email"],
                    id_long=participante["participante_id"],
                    cc=cc_recipients,
                )
                
                logger.info(
                    "Recordatorio enviado participant_id=%s",
                    participante["participante_id"],
                )
                return 1
                
        except Exception:
            logger.exception(
                "Error enviando recordatorio participant_id=%s",
                participante["participante_id"],
            )
        
        return 0

        
async def enviar_recordatorios_pendientes(redis_client, max_concurrent=5, project_configs=None):
    """Envía recordatorios a todos los participantes con estado 'preregistro_completado'"""
    project_configs = project_configs or _PROJECT_CONFIGS
    participantes = get_participantes_pendientes_recordatorio(redis_client, project_configs)
    logger.info(
        "Participantes pendientes de encuesta nacional: %s",
        len(participantes),
    )
    
    if not participantes:
        return 0
    
    logger.info(
        "Iniciando envío concurrente de recordatorios con %s workers",
        max_concurrent,
    )
    
    semaphore = asyncio.Semaphore(max_concurrent)
    tareas = [
        enviar_recordatorio_individual(participante, redis_client, semaphore, project_configs)
        for participante in participantes
    ]
    resultados = await asyncio.gather(*tareas, return_exceptions=True)
    
    recordatorios_enviados = sum(
        resultado for resultado in resultados 
        if isinstance(resultado, int)
    )
    
    logger.info(
        "Total recordatorios enviados: %s",
        recordatorios_enviados,
    )
    return recordatorios_enviados


def get_participantes_pendientes_recordatorio(redis_client, project_configs):
    participantes = []
    cursor = 0
    
    while True:
        cursor, keys = redis_client.scan(
            cursor=cursor,
            match="participante:*",
            count=100
        )
        
        if keys:
            # Pipeline para obtener múltiples hashes de redis
            pipe = redis_client.pipeline()
            for key in keys:
                pipe.hgetall(key)
            results = pipe.execute()
            
            for key, data in zip(keys, results):
                if data.get("estado") == "preregistro_completado":
                    participante_id = key.split(":")[-1]
                    project_id = data.get("project_id")
                    reminder_enabled = _as_bool(data.get("reminder_enabled"), default=False)
                    if not reminder_enabled:
                        continue
                    reminder_url = (data.get("reminder_url") or "").strip()
                    if not reminder_url:
                        continue
                    participantes.append({
                        'participante_id': participante_id,
                        'email': data.get("email"),
                        'project_id': project_id,
                        'project_name': data.get("project_name"),
                        'reminder_enabled': data.get("reminder_enabled"),
                        'reminder_url': reminder_url,
                    })
        
        if cursor == 0:
            break
    
    return participantes



################# Envío de correos pendientes en caso de fallos (backup)##################

async def _enviar_pendiente_individual(key, data, redis_client, semaphore, project_configs):
    async with semaphore:
        try:
            participant_id = key.split(":", 1)[1]
            email = data.get("email")
            estado = data.get("estado")
            project_id = data.get("project_id")
            project_config = project_configs.get(str(project_id), {})
            project_name = data.get("project_name") or project_config.get("project_name") or "Proyecto"
            next_form_url = data.get("next_form_url")

            if not email or "@" not in email:
                logger.warning(
                    "Email inválido para reenvío pendiente participant_id=%s",
                    participant_id,
                )
                return (0, 1)

            # Generar (subject, message) según estado
            if estado == "preregistro_completado":
                if not next_form_url:
                    logger.warning(
                        "URL de preregistro faltante en pendiente; se enviara correo sin link project_id=%s participant_id=%s",
                        project_id,
                        participant_id,
                    )
                try:
                    subject, message = get_preregistro_backup_email(
                        participant_id,
                        project_id=project_id,
                        project_name=project_name,
                        next_form_url=next_form_url,
                    )
                except ValueError as e:
                    logger.error(
                        "Error de plantilla en reenvio pendiente project_id=%s participant_id=%s error=%s",
                        project_id,
                        participant_id,
                        str(e),
                    )
                    return (0, 1)
            elif estado == "encuesta_nacional_completada":
                subject, message = correo_agradecimiento_backup(participant_id)
            else:
                logger.warning(
                    "Estado desconocido para reenvío pendiente participant_id=%s estado=%s",
                    participant_id,
                    estado,
                )
                return (0, 1)

            success = await send_email(
                subject=subject,
                html_message=message,
                recipient=email,
                id_long=participant_id,
                cc=resolve_cc(project_config=project_config),
            )

            if success:
                # Marcar como enviado (backup=0) en la misma key exacta
                redis_client.hset(key, "backup", "0")
                # lectura para confirmar
                val = redis_client.hget(key, "backup")
                logger.info(
                    "Reenvío pendiente exitoso; backup=%s",
                    val,
                )
                return (1, 0)
            else:
                logger.error(
                    "Falló reenvío pendiente participant_id=%s",
                    participant_id,
                )
                return (0, 1)

        except Exception:
            logger.exception(
                "Error procesando reenvío pendiente participant_id=%s",
                participant_id,
            )
            return (0, 1)


async def enviar_correos_pendientes(max_concurrent=5, project_configs=None):
    """Reenvía todos los correos con backup = 1 en redis"""
    project_configs = project_configs or _PROJECT_CONFIGS
    redis_client = get_redis_client()

    # Buscar pendientes con SCAN
    pendientes = []
    cursor = 0
    while True:
        cursor, keys = redis_client.scan(cursor=cursor, match="participante:*", count=500)
        if keys:
            # Pipeline para obtener múltiples hashes
            pipe = redis_client.pipeline()
            for k in keys:
                pipe.hgetall(k)
            results = pipe.execute()

            for k, data in zip(keys, results):
                if data and data.get("backup") == "1":
                    pendientes.append((k, data))

        if cursor == 0:
            break

    if not pendientes:
        logger.info("No hay correos pendientes (backup=1)")
        return 0, 0

    logger.info(
        "Encontrados %s correos pendientes para enviar",
        len(pendientes),
    )

    semaphore = asyncio.Semaphore(max_concurrent)
    tareas = [
        _enviar_pendiente_individual(k, d, redis_client, semaphore, project_configs)
        for (k, d) in pendientes
    ]
    resultados = await asyncio.gather(*tareas, return_exceptions=False)

    sent_count = sum(s for (s, f) in resultados)
    failed_count = sum(f for (s, f) in resultados)
    logger.info(
        "Envío de pendientes completado: %s enviados, %s fallidos",
        sent_count,
        failed_count,
    )
    return sent_count, failed_count
