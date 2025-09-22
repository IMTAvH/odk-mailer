from datetime import datetime
from utils import correo_encuesta_nac_backup, correo_agradecimiento_backup
from utils import correo_recordatorio
from mailer import send_email_sync
import concurrent.futures
import asyncio
import traceback
import os
import redis

def get_redis_client():
    """Función local para obtener cliente Redis"""
    return redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6380)),
        decode_responses=True,
        db=0
    )

################# Envío de correos de recordatorios ##################

async def enviar_recordatorio_individual(participante, redis_client, semaphore, executor):
    async with semaphore:
        try:
            ultimo_recordatorio_key = f"recordatorio:ultimo:{participante['participante_id']}"
            ahora = int(datetime.now().timestamp())
            
            # Solo se crea si no existe
            if redis_client.set(ultimo_recordatorio_key, str(ahora), nx=True, ex=604800):  # 7 días
                # La clave se crea y envia recordatorio
                subject, message = correo_recordatorio(participante)
                
                loop = asyncio.get_event_loop()
                await loop.run_in_executor(
                    executor,
                    lambda: send_email_sync(participante['email'], subject, message, id_long=None)
                )
                
                print(f"📨 Recordatorio enviado: {participante['participante_id']}")
                return 1
                
        except Exception as e:
            print(f"❌ Error enviando recordatorio a {participante['participante_id']}: {e}")
        
        return 0

        
async def enviar_recordatorios_pendientes(redis_client, max_concurrent=2):
    """Envía recordatorios a todos los participantes con estado 'preregistro_completado'"""
    participantes = get_participantes_pendientes_encuesta_nacional(redis_client)
    print(f"🔍 Participantes pendientes de encuesta nacional: {len(participantes)}")
    
    if not participantes:
        return 0
    
    print(f"🚀 Iniciando envío SIMULTÁNEO con {max_concurrent} threads...")
    
    semaphore = asyncio.Semaphore(max_concurrent)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent)
    
    try:
        tareas = [
            enviar_recordatorio_individual(participante, redis_client, semaphore, executor) 
            for participante in participantes
        ]
        
        resultados = await asyncio.gather(*tareas, return_exceptions=True)
        
    finally:
        executor.shutdown(wait=True)  # Cerrar hilos
    
    recordatorios_enviados = sum(
        resultado for resultado in resultados 
        if isinstance(resultado, int)
    )
    
    print(f"📊 Total recordatorios enviados: {recordatorios_enviados}")
    return recordatorios_enviados


def get_participantes_pendientes_encuesta_nacional(redis_client):
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
                    participantes.append({
                        'participante_id': participante_id,
                        'email': data.get("email")
                    })
        
        if cursor == 0:
            break
    
    return participantes



################# Envío de correos pendientes en caso de fallos ##################

async def _enviar_pendiente_individual(key, data, redis_client, executor, semaphore):
    async with semaphore:
        try:
            participant_id = key.split(":", 1)[1]
            email = data.get("email")
            estado = data.get("estado")

            if not email or "@" not in email:
                print(f"⚠️ Email inválido para {participant_id}: {email!r}")
                return (0, 1)

            # Generar (subject, message) según estado
            if estado == "preregistro_completado":
                subject, message = correo_encuesta_nac_backup(participant_id)
            elif estado == "encuesta_nacional_completada":
                subject, message = correo_agradecimiento_backup(participant_id)
            else:
                print(f"⚠️ Estado desconocido para {participant_id}: {estado!r}")
                return (0, 1)

            # Enviar por thread
            loop = asyncio.get_running_loop()
            success = await loop.run_in_executor(
                executor,
                lambda: send_email_sync(email, subject, message, participant_id)
            )

            if success:
                # Marcar como enviado (backup=0) en la misma key exacta
                redis_client.hset(key, "backup", "0")
                # lectura para confirmar
                val = redis_client.hget(key, "backup")
                print(f"✅ Enviado y backup={val} para {participant_id} (key: {key})")
                return (1, 0)
            else:
                print(f"❌ Falló reenvío para {participant_id}")
                return (0, 1)

        except Exception as e:
            print(f"❌ Error procesando {key}: {e}")
            print(traceback.format_exc())
            return (0, 1)


async def enviar_correos_pendientes(max_concurrent=2):
    """Reenvía todos los correos con backup = 1 en redis"""
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
        print("📭 No hay correos pendientes (backup = 1)")
        return 0, 0

    print(f"📬 Encontrados {len(pendientes)} correos pendientes para enviar")

    semaphore = asyncio.Semaphore(max_concurrent)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_concurrent)

    try:
        tareas = [
            _enviar_pendiente_individual(k, d, redis_client, executor, semaphore)
            for (k, d) in pendientes
        ]
        resultados = await asyncio.gather(*tareas, return_exceptions=False)
    finally:
        executor.shutdown(wait=True)

    sent_count = sum(s for (s, f) in resultados)
    failed_count = sum(f for (s, f) in resultados)
    print(f"📊 Envío completado: {sent_count} enviados, {failed_count} fallidos")
    return sent_count, failed_count