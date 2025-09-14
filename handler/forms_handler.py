import os
from utils import correo_encuesta_nac, correo_agradecimiento

async def handle_preregistro(parsed, form_id, project_id, redis_client):
    """Maneja Laura2-piloto-encuesta-preregistro"""
    if project_id != os.getenv("ODK_PROJECT_ID"):
        return None, None, None
        
    email_from_form = parsed["data"]["participantes"]["correo"]
    participante_id_long = parsed["data"]["participantes"]["participante_id"]
    participante_id_short = parsed["data"]["participantes"]["short_id"]
    
    if email_from_form:
        if participante_id_long:
            redis_client.setex(f"webhook:email:long:{participante_id_long}", 604800, email_from_form)
            redis_client.setex(f"webhook:email:form:preRegistro:{participante_id_long}", 604800, email_from_form)
            print(f"📧 Email guardado (long): {participante_id_long} -> {email_from_form}")
        if participante_id_short:
            redis_client.setex(f"webhook:email:short:{participante_id_short}", 604800, email_from_form)
            print(f"📧 Email guardado (short): {participante_id_short} -> {email_from_form}")
    
    return correo_encuesta_nac(parsed)


async def handle_encuesta_principal(parsed, form_id, project_id, redis_client):
    """Maneja Laura2-piloto-encuesta"""
    if project_id != os.getenv("ODK_PROJECT_ID"):
        return None, None, None
        
    short_id = parsed["data"]["preamble"]["entity_details"]["short_id"]
    long_id = parsed["data"]["preamble"]["entity_details"]["long_id"]
    status = ""
    
    cached_email = None
    if long_id:
        cached_email = redis_client.get(f"webhook:email:long:{long_id}")
        if cached_email:
            redis_client.delete(f"webhook:email:form:preRegistro:{long_id}")
            redis_client.setex(f"webhook:email:form:EncNacional:{long_id}",604800, cached_email)
            print(f"Email encontrado en cache (long_id): {cached_email}")
    if not cached_email and short_id:
        cached_email = redis_client.get(f"webhook:email:short:{short_id}")
        if cached_email:
            print(f"Email encontrado en cache (short_id): {cached_email}")
    
    if cached_email:
        subject, message = correo_agradecimiento(parsed)
        return cached_email, subject, message
    
    return None, None, None