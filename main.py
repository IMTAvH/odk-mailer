from fastapi import FastAPI, BackgroundTasks
from fastapi import Request
import xmltodict
from dotenv import load_dotenv
import os
from mailer import send_email
from utils import is_duplicate
#from search_by_odk_api import buscar_submissions_en_p1, buscar_submissions_en_p2, buscar_submissions_en_p3
import redis
from handler.forms_handler import handle_preregistro, handle_encuesta_principal

load_dotenv()

app = FastAPI()

r = redis.Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6380)),  # Puerto 6380
    decode_responses=True,
    db=0
)

try:
    r.ping()
    print("✅ Conexión a Redis exitosa")
except:
    print("❌ Error conectando a Redis")

# Procesar en background
async def process_webhook_async(body: dict):
    """Procesa el webhook de forma asíncrona en background"""
    try:
        print("🔄 Procesando webhook en background...")
        raw_xml = body.get("data", {}).get("xml") or body.get("data", {}).get("xml_content")

        if not raw_xml:
            print("❌ No se encontró XML en el payload")
            return

        parsed = xmltodict.parse(raw_xml)
        form_id = parsed["data"].get("@id")
        instance_id = parsed["data"]["meta"].get("instanceID")
        version = parsed["data"].get("@version")
        project_id = version.split("-")[-1] if version and "-" in version else None
        print(f"🆔 Form ID: {form_id}, Instance ID: {instance_id}, Version: {version}, projectId: {project_id}")

        if is_duplicate(instance_id):
            print(f"⚠️ Duplicate ignored: {instance_id}")
            return

        email = None

        FORM_HANDLERS = {
            "Laura2-piloto-encuesta-preregistro": handle_preregistro,
            "Laura2-piloto-encuesta": handle_encuesta_principal
        }

        if form_id in FORM_HANDLERS:
            email, subject, message = await FORM_HANDLERS[form_id](parsed, form_id, project_id, r)
        else:
            print(f"⚠️ Formulario no manejado: {form_id}")
            return
        

        '''
        if form_id == "Laura2-piloto-encuesta-preregistro" and project_id == os.getenv("ODK_PROJECT_ID"):
            print("Guardando email en Redis...")
            email_from_form = parsed["data"]["participantes"]["correo"]
            
            # Usar AMBOS IDs como clave para máxima compatibilidad
            participante_id_long = parsed["data"]["participantes"]["participante_id"]  # ID largo
            participante_id_short = parsed["data"]["participantes"]["short_id"]        # ID corto
            
            if email_from_form:
                # Guardar con ambos IDs como clave
                if participante_id_long:
                    r.setex(f"webhook:email:long:{participante_id_long}", 604800, email_from_form)
                    print(f"Email guardado (long): {participante_id_long} -> {email_from_form}")
                
                if participante_id_short:
                    r.setex(f"webhook:email:short:{participante_id_short}", 604800, email_from_form)
                    print(f"Email guardado (short): {participante_id_short} -> {email_from_form}")
            
            email, subject, message = correo_encuesta_nac(parsed)
        '''
            
        # Commented-out code for future reference
        # elif form_id == "Laura2-piloto-encuesta-ic":
        #     participant_id = parsed["data"]["preamble"].get("part_id")
        #     consentimiento = parsed["data"]["consent"].get("Q0_accept_consent")
        #     print("🔎 participant_id (desde part_id):", participant_id)
        #     if consentimiento == "yes":
        #         email, subject, message = correo_encuesta_nac(participant_id, parsed)
        #     else:
        #         print("Participante no acepto el consentimiento informado")
        #         email = None
        '''
        elif form_id == "Laura2-piloto-encuesta" and project_id == os.getenv("ODK_PROJECT_ID"):
            print("🔍 Buscando email en Redis...")
            
            # Extraer los IDs del segundo formulario
            short_id = parsed["data"]["preamble"]["entity_details"]["short_id"]
            long_id = parsed["data"]["preamble"]["entity_details"]["long_id"]
            
            cached_email = None
            
            # Buscar primero por long_id, luego por short_id
            if long_id:
                cached_email = r.get(f"webhook:email:long:{long_id}")
                if cached_email:
                    print(f"Email encontrado en cache (long_id): {cached_email}")
            
            if not cached_email and short_id:
                cached_email = r.get(f"webhook:email:short:{short_id}")
                if cached_email:
                    print(f"Email encontrado en cache (short_id): {cached_email}")
            
            if cached_email:
                subject, message = correo_agradecimiento(parsed)
                email = cached_email  # Override 
            else:
                print("⚠️ Email no encontrado en cache.")
                email = None
        '''

        #elif form_id == "Laura2-piloto-encuesta-p2":
        #    participant_id = parsed["data"]["preamble"].get("part_id_3")
        #    complete_p1 = buscar_submissions_en_p1(participant_id)
        #    complete_p3 = buscar_submissions_en_p3(participant_id)
        #    if complete_p1 == 'yes' and complete_p3 == 'yes':
        #        email, subject, message = correo_agradecimiento(parsed)
        #    else:
        #        email = None

        #elif form_id == "Laura2-piloto-encuesta-p3":
        #    participant_id = parsed["data"]["preamble"].get("part_id_4")
        #    complete_p1 = buscar_submissions_en_p1(participant_id)
        #    complete_p2 = buscar_submissions_en_p2(participant_id)
        #    if complete_p1 == 'yes' and complete_p2 == 'yes':
        #        email, subject, message = correo_agradecimiento(parsed)
        #    else:
        #        email = None

        #elif form_id == "Laura2-piloto-asignacion":
        #    email, subject, message = correo_asignacion_tc(parsed)

        #elif form_id == "Laura2-piloto-agendamiento":
        #    mes_visita = parsed["data"].get("mes_visita")
        #    numero_visita = parsed["data"].get("numero_visita")
            
        #    if mes_visita == 'm1' and numero_visita == 'v1':
        #        email, subject, message = correo_agendamiento_m1v1(parsed)
        #    elif mes_visita == 'm1' and numero_visita == 'v2':
        #        email, subject, message = correo_agendamiento_m1v2(parsed)
        #    elif mes_visita == 'm1' and numero_visita == 'v3':
        #        email, subject, message = correo_agendamiento_m1v3(parsed)
        #    elif mes_visita == 'm2' and numero_visita == 'v1':
        #        email, subject, message = correo_agendamiento_m2v1(parsed)
        #    elif mes_visita == 'm2' and numero_visita == 'v2':
        #        email, subject, message = correo_agendamiento_m2v2(parsed)
        #    elif mes_visita == 'm2' and numero_visita == 'v3':
        #        email, subject, message = correo_agendamiento_m2v3(parsed)
        #    else:
        #        email = None

        if email:
            print(f"✅ Enviando correo a {email} (ID: {instance_id})")
            await send_email(subject=subject, html_message=message, recipient=email)
            print(f"✅ Correo enviado a {email}")
        else:
            print(f"⚠️ No se encontró correo para ID: {instance_id}")
            
    except Exception as e:
        print(f"❌ Error procesando webhook: {e}")

# Responde inmediatamente y procesa en background
@app.post("/hooks")
async def receive_webhook(req: Request, background_tasks: BackgroundTasks):
    try:

        body = await req.json()
        print("📩 Webhook recibido")
        print("📄 body:", body)
        # RESPUESTA INMEDIATA - No espera el procesamiento
        background_tasks.add_task(process_webhook_async, body)
        
        # Respuesta en <100ms
        return {"status": "accepted", "message": "Processing in background"}
        
    except Exception as e:
        print(f"❌ Error recibiendo webhook: {e}")
        return {"status": "error", "message": str(e)}