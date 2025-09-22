import os
from utils import correo_encuesta_nac, correo_agradecimiento, correo_encuesta_nac_backup, EMAIL_CAS_LUA

async def handle_preregistro(parsed, form_id, project_id, redis_client):
    """Maneja Laura2-piloto-encuesta-preregistro"""
    if project_id != os.getenv("ODK_PROJECT_ID"):
        return None, None, None, None
        
    email_from_form = parsed["data"]["participantes"]["correo"]
    participante_id_long = parsed["data"]["participantes"]["participante_id"]
    
    if email_from_form:
        if participante_id_long:
                        
            participante_data = {
                "email": email_from_form,
                "estado": "preregistro_completado",
                "backup": "0"
            }

            redis_client.hset(f"participante:{participante_id_long}", mapping=participante_data)
            redis_client.expire(f"participante:{participante_id_long}", 3888000)

            print(f"📧 Email guardado (long): {participante_id_long} -> {email_from_form}")

            email, subject, message = correo_encuesta_nac(parsed)
            return email, subject, message, participante_id_long

    return None, None, None, None


async def handle_encuesta_principal(parsed, form_id, project_id, redis_client):
    """Maneja Laura2-piloto-encuesta"""
    if project_id != os.getenv("ODK_PROJECT_ID"):
        return None, None, None, None
    
    long_id = parsed["data"]["preamble"]["entity_details"]["long_id"]
    
    cached_email = None
    if long_id:
        participante_data = redis_client.hgetall(f"participante:{long_id}")
        if participante_data and participante_data.get("email"):
            cached_email = participante_data["email"]

            # Actualizar estado a completado
            redis_client.hset(f"participante:{long_id}", "estado", "encuesta_nacional_completada")
            redis_client.hset(f"participante:{long_id}", "backup", "0") 

            print(f"Email encontrado en cache (long_id): {cached_email}")

    if not cached_email: 
        print(f"Email no encontrado en cache (long_id)")
    
    if cached_email:
        subject, message = correo_agradecimiento(parsed)
        return cached_email, subject, message, long_id
    
    return None, None, None, None

async def actualizar_email_participante(participante_id: str, email: str, redis_client):

    if not participante_id or not email:
        return None, None

    key = f"participante:{participante_id}"
    try:

        new_email = email.strip().lower()

        result = redis_client.eval(EMAIL_CAS_LUA, 1, key, new_email)

        if result == 0:
            print(f"⚠️ No se encontró participante con ID largo {participante_id} en Redis")
            return None, None

        if result == 1:
            print(f"ℹ️ Email idéntico, no se actualiza: {key}")
            return None, None

        print(f"✅ Actualizado email en {key}")

        # Genera el contenido del correo de email actualizado
        subject, message = correo_encuesta_nac_backup(participante_id)
        return subject, message

    except Exception as e:
        print(f"⚠️ Error actualizando email en Redis para {key}: {e}")
        return None, None
