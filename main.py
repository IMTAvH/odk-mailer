from fastapi import FastAPI, BackgroundTasks
from fastapi import Request
import xmltodict
from dotenv import load_dotenv
import os
from mailer import send_email
from utils import is_duplicate
from reminder.form_reminder import enviar_recordatorios_pendientes, enviar_correos_pendientes
import redis
from handler.forms_handler import handle_preregistro, handle_encuesta_principal, actualizar_email_participante
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import pytz
from contextlib import asynccontextmanager

load_dotenv()

tz = pytz.timezone('America/Lima')

scheduler = AsyncIOScheduler(timezone=tz)

async def tarea_recordatorios_semanales():
    """ejecuta periódicamente para enviar recordatorios"""
    try:
        logger.info("Iniciando envío de recordatorios semanales")
        count = await enviar_recordatorios_pendientes(r)
        logger.info(f"✅ Recordatorios semanales completados: {count} enviados")
    except Exception as e:
        logger.error(f"❌ Error en recordatorios semanales: {e}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Al iniciar
    logger.info("Iniciando")

    # Enviar correos pendientes al iniciar (backup = 1 en redis)
    logger.info("Enviando correos pendientes al iniciar...")
    try:
        sent, failed = await enviar_correos_pendientes()
        logger.info(f"✅ Correos pendientes al inicio: {sent} enviados, {failed} fallidos")
    except Exception as e:
        logger.error(f"❌ Error enviando correos pendientes al inicio: {e}")
    
    # Configurar la tarea para que se ejecute peridicamente con hora de Lima/Perú
    day=os.getenv('WEEK_DAY','sat')
    hour=int(os.getenv('DAY_HOUR',9))
    minute=int(os.getenv('DAY_MIN',0))

    scheduler.add_job(
        func=tarea_recordatorios_semanales,
        trigger=CronTrigger(day_of_week=day, hour=hour, minute=minute, timezone=tz),
        id='run_reminders_weekly',
        replace_existing=True,
        misfire_grace_time=3600,
        coalesce=True
    )
    
    if not scheduler.running:
        scheduler.start()
    logger.info(f"Scheduler iniciado - Recordatorios programados para cada {day} a las {hour}:{minute:02d} hrs")
    
    yield
    
    # Al terminar el fastapi
    logger.info("Cerrando aplicación")
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler detenido")


app = FastAPI(lifespan=lifespan)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_redis_client():

    r = redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6380)),
        decode_responses=True,
        db=0
    )

    return r

r = get_redis_client()

try:
    r.ping()
    logger.info("Conexión a Redis exitosa")
except Exception as e:
    logger.error(f"Error conectando a Redis: {e}")


        
# Procesar en background
async def process_webhook_async(body: dict):
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
            email, subject, message, id_long = await FORM_HANDLERS[form_id](parsed, form_id, project_id, r)
        else:
            print(f"⚠️ Formulario no manejado: {form_id}")
            return
        

        if email:
            print(f"✅ Enviando correo a {email} (ID: {instance_id})")
            await send_email(subject=subject, html_message=message, recipient=email, id_long=id_long)
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
        # Respuesta inmmediata - No espera el procesamiento
        background_tasks.add_task(process_webhook_async, body)
        
        return {"status": "accepted", "message": "Processing in background"}
        
    except Exception as e:
        print(f"❌ Error recibiendo webhook: {e}")
        return {"status": "error", "message": str(e)}
    
    
@app.post("/update-participantes")
async def update_participantes(req: Request, background_tasks: BackgroundTasks):
    try:
        body = await req.json()
        print("📩 Update participantes recibido")
        print("📄 body:", body)
        
        parsed = body.get("data", {})

        if not parsed:
            print("❌ No se encontró XML en el payload")
            return {"status": "error", "message": "XML no encontrado en payload"}
        
        email_update = parsed.get('email')
        participant_long_id = parsed.get('long_id')
        print(f"Nuevo correo {email_update} del Participante {participant_long_id}")

        subject, message = await actualizar_email_participante(participant_long_id, email_update, r)

        if subject and message:
            print(f"✅ Enviando correo a {email_update} (ID: {participant_long_id})")
            background_tasks.add_task(
                send_email,
                subject=subject,
                html_message=message,
                recipient=email_update,
                id_long=participant_long_id
            )
            print(f"✅ Correo enviado a {email_update}")
            return {"status": "accepted", "message": f"Actualizacion de correo en cola para {email_update}"}
        else:
            return {"status": "accepted", "message": "No se encontró un participante coincidente en caché o no se proporcionó un correo."}

    except Exception as e:
        print(f"❌ Error recibiendo update-participantes: {e}")
        return {"status": "error", "message": str(e)}