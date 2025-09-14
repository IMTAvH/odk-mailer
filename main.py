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