import logging
from templates import correo_preregistro_imvaha
from config.form_routes import (
    resolve_next_form_url,
    resolve_route_reminder_enabled,
    resolve_route_reminder_url,
)
from handler.helpers import _get_nested, _save_participant

logger = logging.getLogger(__name__)


async def handle_imvaha_preregistro(parsed, form_id, project_id, redis_client, route_config=None):
    """Maneja IMVAHA_prereg_pe_es (project_id=9)."""
    route_config = route_config or {}
    email_from_form = _get_nested(parsed, "data", "IMVAHA", "personal_information", "email")
    participante_id_long = _get_nested(parsed, "data", "IMVAHA", "registration", "long_id")
    next_form_url = resolve_next_form_url(route_config)
    reminder_enabled = resolve_route_reminder_enabled(route_config)
    reminder_url = resolve_route_reminder_url(route_config)
    project_name = route_config.get("project_name", "IMVAHA")

    if not participante_id_long:
        logger.warning(
            "Payload IMVAHA preregistro sin participant_id project_id=%s form_id=%s",
            project_id,
            form_id,
        )
        return None, None, None, None

    if not email_from_form:
        return None, None, None, participante_id_long

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
        "Email guardado en cache para preregistro IMVAHA project_id=%s participant_id=%s",
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

    email, subject, message = correo_preregistro_imvaha(
        email=email_from_form,
        short_id=participante_id_long[:6],
        next_form_url=next_form_url,
    )
    return email, subject, message, participante_id_long
