from fastapi import FastAPI, BackgroundTasks
from fastapi import Request
from fastapi.staticfiles import StaticFiles
import xmltodict
from dotenv import load_dotenv
import os
from uuid import uuid4
from mail.mailer import send_email
from utils import is_duplicate
from reminder.form_reminder import enviar_recordatorios_pendientes, enviar_correos_pendientes
import redis
from handler.forms_handler import HANDLER_REGISTRY, actualizar_email_participante
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
import pytz
from contextlib import asynccontextmanager
from audit.logging_config import configure_logging
from config.form_routes import load_form_routes, resolve_cc

load_dotenv()
configure_logging()

logger = logging.getLogger(__name__)

tz = pytz.timezone('America/Lima')

scheduler = AsyncIOScheduler(timezone=tz)

FORM_ROUTES, PROJECT_CONFIGS = load_form_routes()
logger.info(
    "Rutas de formularios cargadas: %s, proyectos cargados: %s",
    len(FORM_ROUTES),
    len(PROJECT_CONFIGS),
)


async def tarea_recordatorios_semanales():
    """ejecuta periódicamente para enviar recordatorios"""
    try:
        logger.info("Iniciando envío de recordatorios semanales")
        count = await enviar_recordatorios_pendientes(r, project_configs=PROJECT_CONFIGS)
        logger.info("Recordatorios semanales completados: %s enviados", count)
    except Exception:
        logger.exception("Error en recordatorios semanales")

@asynccontextmanager
async def lifespan(app):
    # Al iniciar
    logger.info("Iniciando")

    # Controla si se drenan pendientes al arranque:
    # true => intenta enviar backup=1; false => no procesa pendientes en startup.
    if os.getenv("SEND_PENDING_ON_STARTUP", "false").strip().lower() == "true":
        logger.info("Enviando correos pendientes al iniciar...")
        try:
            sent, failed = await enviar_correos_pendientes(project_configs=PROJECT_CONFIGS)
            logger.info(
                "Correos pendientes procesados al inicio: %s enviados, %s fallidos",
                sent,
                failed,
            )
        except Exception:
            logger.exception("Error enviando correos pendientes al inicio")
    else:
        logger.info("Envio de pendientes al inicio desactivado")
    
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
    logger.info(
        "Scheduler iniciado: cada %s a las %s:%s",
        day,
        hour,
        f"{minute:02d}",
    )
    
    yield
    
    # Al terminar el fastapi
    logger.info("Cerrando aplicación")
    if scheduler.running:
        scheduler.shutdown()
        logger.info("Scheduler detenido")


app = FastAPI(lifespan=lifespan)

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
except Exception:
    logger.exception("Error conectando a Redis")


# Funciones para extraer datos del xml y enviarlos hacia el mailer
async def process_webhook_async(body, request_id):
    try:
        logger.info("Procesando webhook en background request_id=%s", request_id)
        raw_xml = body.get("data", {}).get("xml") or body.get("data", {}).get("xml_content")

        if not raw_xml:
            logger.warning("Webhook sin XML en payload request_id=%s", request_id)
            return

        parsed = xmltodict.parse(raw_xml)
        data = parsed.get("data", {})
        meta = data.get("meta", {})
        form_id = data.get("@id")
        instance_id = meta.get("instanceID")
        version = data.get("@version")
        project_id = version.split("-")[-1] if version and "-" in version else None
        logger.info(
            "Webhook parseado request_id=%s form_id=%s instance_id=%s version=%s project_id=%s",
            request_id,
            form_id,
            instance_id,
            version,
            project_id,
        )

        # Ejemplo de payload esperado:

        # form_id: IMVAHA_prereg_pe_es
        # instance_id: uuid:815884a6-da11-4e2a-8901-34b36daf0756
        # version: 20260224a-9
        # project_id: 9

        if not instance_id:
            logger.warning("Webhook sin instance_id request_id=%s form_id=%s", request_id, form_id)
            return

        if is_duplicate(instance_id):
            logger.warning("Webhook duplicado ignorado request_id=%s instance_id=%s", request_id, instance_id)
            return

        email = None

        route_key = (str(project_id), str(form_id))
        route_config = FORM_ROUTES.get(route_key)
        if not route_config:
            logger.warning(
                "Formulario no manejado request_id=%s form_id=%s project_id=%s",
                request_id,
                form_id,
                project_id,
            )
            return

        handler_name = route_config.get("handler")
        form_handler = HANDLER_REGISTRY.get(handler_name)
        if not form_handler:
            logger.error(
                "Handler no registrado request_id=%s form_id=%s project_id=%s handler=%s",
                request_id,
                form_id,
                project_id,
                handler_name,
            )
            return

        email, subject, message, id_long = await form_handler(
            parsed,
            form_id,
            project_id,
            r,
            route_config=route_config,
        )

        if email:
            project_config = PROJECT_CONFIGS.get(str(project_id), {})
            cc_recipients = resolve_cc(route_config=route_config, project_config=project_config)
            logger.info(
                "Enviando correo request_id=%s instance_id=%s form_id=%s",
                request_id,
                instance_id,
                form_id,
            )
            sent = await send_email(
                subject=subject,
                html_message=message,
                recipient=email,
                id_long=id_long,
                cc=cc_recipients,
            )
            if sent:
                logger.info(
                    "Correo enviado request_id=%s instance_id=%s form_id=%s",
                    request_id,
                    instance_id,
                    form_id,
                )
            else:
                logger.error(
                    "Fallo al enviar correo request_id=%s instance_id=%s form_id=%s",
                    request_id,
                    instance_id,
                    form_id,
                )
        else:
            if route_config.get("email_optional"):
                logger.info(
                    "No se envia correo: email opcional vacio request_id=%s instance_id=%s form_id=%s",
                    request_id,
                    instance_id,
                    form_id,
                )
            else:
                logger.warning(
                    "No se encontro correo para envio request_id=%s instance_id=%s form_id=%s",
                    request_id,
                    instance_id,
                    form_id,
                )

    except Exception:
        logger.exception("Error procesando webhook request_id=%s", request_id)


# Responde inmediatamente y procesa en background
@app.post("/hooks")
async def receive_webhook(req: Request, background_tasks: BackgroundTasks):
    request_id = req.headers.get("X-Request-ID", uuid4().hex)
    try:

        body = await req.json()
        logger.info("Webhook recibido request_id=%s", request_id)
        # Respuesta inmmediata - No espera el procesamiento
        background_tasks.add_task(process_webhook_async, body, request_id)

        return {"status": "accepted", "message": "Processing in background"}

    except Exception:
        logger.exception("Error recibiendo webhook request_id=%s", request_id)
        return {"status": "error", "message": "Error processing webhook"}
    

@app.post("/update-participantes")
async def update_participantes(req: Request, background_tasks: BackgroundTasks):
    request_id = req.headers.get("X-Request-ID", uuid4().hex)
    try:
        body = await req.json()
        logger.info("Update participantes recibido request_id=%s", request_id)

        parsed = body.get("data", {})

        if not parsed:
            logger.warning("Payload sin data para update-participantes request_id=%s", request_id)
            return {"status": "error", "message": "XML no encontrado en payload"}

        email_update = parsed.get('email')
        participant_long_id = parsed.get('long_id')
        logger.info(
            "Solicitud de actualizacion de correo request_id=%s participant_id=%s",
            request_id,
            participant_long_id,
        )

        subject, message = await actualizar_email_participante(participant_long_id, email_update, r)

        if subject and message:
            participant_data = r.hgetall(f"participante:{participant_long_id}") or {}
            project_id_for_send = parsed.get("project_id") or participant_data.get("project_id")
            project_config = PROJECT_CONFIGS.get(str(project_id_for_send), {})
            cc_recipients = resolve_cc(project_config=project_config)
            logger.info(
                "Encolando correo de actualización request_id=%s participant_id=%s",
                request_id,
                participant_long_id,
            )
            background_tasks.add_task(
                send_email,
                subject=subject,
                html_message=message,
                recipient=email_update,
                id_long=participant_long_id,
                cc=cc_recipients,
            )
            return {"status": "accepted", "message": f"Actualizacion de correo en cola para {email_update}"}
        else:
            logger.warning("No hubo actualizacion de correo request_id=%s participant_id=%s", request_id, participant_long_id)
            return {"status": "accepted", "message": "No se encontro un participante coincidente en cache o no se proporcionó un correo."}

    except Exception:
        logger.exception("Error recibiendo update-participantes request_id=%s", request_id)
        return {"status": "error", "message": "Error processing update"}
