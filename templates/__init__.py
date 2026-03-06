from templates.imvaha import (
    correo_preregistro_backup_imvaha,
    correo_preregistro_imvaha,  # sirven para importar
    correo_recordatorio_imvaha,
)
from templates.laura import (
    correo_agradecimiento,  # sirven para importar
    correo_agradecimiento_backup,  # sirven para importar
    correo_encuesta_nac, # sirven para importar
    correo_encuesta_nac_backup,
    correo_recordatorio,
)


def get_preregistro_backup_email(
    participante,
    project_id,
    project_name,
    next_form_url=None,
):
    project_name = project_name or "Proyecto"
    handlers = {
        "10": correo_encuesta_nac_backup,
        "9": correo_preregistro_backup_imvaha,
    }
    template_fn = handlers.get(str(project_id))
    if not template_fn:
        raise ValueError(
            f"No existe template de preregistro backup para project_id={project_id}"
        )
    return template_fn(
        participante,
        next_form_url=next_form_url,
        project_name=project_name,
    )


def get_reminder_email(participante, project_id):
    handlers = {
        "10": correo_recordatorio,
        "9": correo_recordatorio_imvaha,
    }
    template_fn = handlers.get(str(project_id))
    if not template_fn:
        raise ValueError(
            f"No existe template de recordatorio para project_id={project_id}"
        )
    return template_fn(participante)
