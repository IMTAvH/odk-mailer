import logging
from templates import (
    correo_agradecimiento,
    correo_encuesta_nac,
    get_preregistro_backup_email,
)
from utils import EMAIL_CAS_LUA
from config.form_routes import (
    resolve_next_form_url,
    resolve_route_reminder_enabled,
    resolve_route_reminder_url,
)
from handler.helpers import _get_nested, _save_participant

logger = logging.getLogger(__name__)


async def handle_laura_preregistro(parsed, form_id, project_id, redis_client, route_config=None):
    """Maneja Laura2-piloto-encuesta-preregistro"""
    route_config = route_config or {}
    email_from_form = _get_nested(parsed, "data", "participantes", "correo")
    participante_id_long = _get_nested(parsed, "data", "participantes", "participante_id")
    next_form_url = resolve_next_form_url(route_config)
    reminder_enabled = resolve_route_reminder_enabled(route_config)
    reminder_url = resolve_route_reminder_url(route_config)
    project_name = route_config.get("project_name", "Laura")

    if not email_from_form or not participante_id_long:
        logger.warning(
            "Payload Laura preregistro incompleto project_id=%s form_id=%s",
            project_id,
            form_id,
        )
        return None, None, None, None

    _save_participant(
        redis_client=redis_client,
        participant_id=participante_id_long,
        email=email_from_form,
        estado="preregistro_completado",
        project_id=project_id,
        project_name=project_name,
        next_form_url=next_form_url,
        reminder_enabled=reminder_enabled,
        reminder_url=reminder_url,
    )

    logger.info(
        "Email guardado en cache para preregistro project_id=%s participant_id=%s",
        project_id,
        participante_id_long,
    )

    if not next_form_url:
        logger.warning(
            "URL faltante para preregistro; se enviara correo sin link project_id=%s form_id=%s participant_id=%s",
            project_id,
            form_id,
            participante_id_long,
        )

    email, subject, message = correo_encuesta_nac(parsed, next_form_url=next_form_url)
    return email, subject, message, participante_id_long


async def handle_laura_encuesta_principal(parsed, form_id, project_id, redis_client, route_config=None):
    """Maneja Laura2-piloto-encuesta"""
    long_id = _get_nested(parsed, "data", "preamble", "entity_details", "long_id")
    if not long_id:
        logger.warning(
            "Payload Laura encuesta incompleto project_id=%s form_id=%s",
            project_id,
            form_id,
        )
        return None, None, None, None

    cached_email = None
    participante_data = redis_client.hgetall(f"participante:{long_id}")
    if participante_data and participante_data.get("email"):
        cached_email = participante_data["email"]

        # Actualizar estado a completado
        redis_client.hset(f"participante:{long_id}", "estado", "encuesta_nacional_completada")
        redis_client.hset(f"participante:{long_id}", "backup", "0")

        logger.info(
            "Email encontrado en cache para encuesta principal project_id=%s participant_id=%s",
            project_id,
            long_id,
        )

    if not cached_email:
        logger.warning(
            "Email no encontrado en cache para encuesta principal project_id=%s participant_id=%s",
            project_id,
            long_id,
        )

    if cached_email:
        subject, message = correo_agradecimiento(parsed)
        return cached_email, subject, message, long_id

    return None, None, None, None


async def actualizar_email_participante(participante_id, email, redis_client):
    if not participante_id or not email:
        return None, None

    key = f"participante:{participante_id}"
    try:
        new_email = email.strip().lower()

        result = redis_client.eval(EMAIL_CAS_LUA, 1, key, new_email)

        if result == 0:
            logger.warning(
                "No se encontró participante para actualizar email participant_id=%s",
                participante_id,
            )
            return None, None

        if result == 1:
            logger.info(
                "Email idéntico, no se requiere actualización participant_id=%s",
                participante_id,
            )
            return None, None

        logger.info(
            "Email actualizado en cache participant_id=%s",
            participante_id,
        )

        participante_data = redis_client.hgetall(key) or {}
        project_id = participante_data.get("project_id")
        next_form_url = participante_data.get("next_form_url")
        project_name = participante_data.get("project_name", "Laura")
        if not next_form_url:
            logger.warning(
                "URL de preregistro faltante en actualizacion de email; se enviara correo sin link participant_id=%s",
                participante_id,
            )

        try:
            subject, message = get_preregistro_backup_email(
                participante_id,
                project_id=project_id,
                project_name=project_name,
                next_form_url=next_form_url,
            )
        except ValueError as e:
            logger.error("Error de plantilla en update participant_id=%s error=%s", participante_id, str(e))
            return None, None
        
        return subject, message

    except Exception:
        logger.exception(
            "Error actualizando email en Redis participant_id=%s",
            participante_id,
        )
        return None, None
