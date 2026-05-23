import asyncio
import os
import threading
import traceback
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import aiosmtplib
import redis
import logging

logger = logging.getLogger(__name__)

# Env esperado:
# EMAIL_MAX_CONCURRENT=int (ej. 5)
# EMAIL_MAX_RETRIES=int (ej. 2)
# EMAIL_RETRY_BACKOFF_SECONDS=float (ej. 1.0)

# cantidad maximo de concurrencia para envio de correos
EMAIL_MAX_CONCURRENT = max(int(os.getenv("EMAIL_MAX_CONCURRENT", "5")), 1)

# maximos reintentos para envio de correos
EMAIL_MAX_RETRIES = max(int(os.getenv("EMAIL_MAX_RETRIES", "2")), 0)

EMAIL_RETRY_BACKOFF_SECONDS = max(float(os.getenv("EMAIL_RETRY_BACKOFF_SECONDS", "1.0")), 0.0)

_SEMAPHORES_BY_LOOP = {}
_SEMAPHORE_LOCK = threading.Lock()


def get_redis_client():
    """Función local para obtener cliente Redis"""
    return redis.Redis(
        host=os.getenv('REDIS_HOST', 'localhost'),
        port=int(os.getenv('REDIS_PORT', 6380)),
        decode_responses=True,
        db=0
    )


def _build_message(subject, recipient, html_message, cc_recipients=None):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = recipient
    if cc_recipients:
        msg["Cc"] = ", ".join(cc_recipients)
    msg.attach(MIMEText(html_message, "html"))
    return msg


# envia los correos de manera concurrente
async def _send_message_async(msg, recipients=None):
    # Solo variables del .env del proyecto:
    # EMAIL_SECURE=true  => SMTPS (TLS implícito)
    # EMAIL_IGNORE_TLS=true => desactiva STARTTLS
    use_tls = os.getenv("EMAIL_SECURE", "false").strip().lower() == "true"
    ignore_tls = os.getenv("EMAIL_IGNORE_TLS", "false").strip().lower() == "true"
    start_tls = not ignore_tls

    if use_tls:
        start_tls = False
    # EMAIL_TIMEOUT_SECONDS=float (ej. 20)
    timeout_seconds = float(os.getenv("EMAIL_TIMEOUT_SECONDS", "20"))
    password = (os.getenv("EMAIL_PASSWORD") or "").replace(" ", "")
    
    await aiosmtplib.send(
        msg,
        recipients=recipients,
        hostname=os.getenv("EMAIL_HOST"),
        port=int(os.getenv("EMAIL_PORT", 587)),
        username=os.getenv("EMAIL_USER"),
        password=password,
        use_tls=use_tls,
        start_tls=start_tls,
        timeout=timeout_seconds,
    )

# Marca en Redis que el participante con id_long tiene un correo pendiente por enviar (backup)
def _mark_backup_pending(id_long):
    if id_long:
        redis_client = get_redis_client()
        redis_client.hset(f"participante:{id_long}", "backup", "1")
        logger.warning("Estado backup actualizado a 1 - correo pendiente participant_id=%s", id_long)

# limitar los envíos concurrentes de correo para evitar saturacion
def _get_email_semaphore():
    loop = asyncio.get_running_loop()
    with _SEMAPHORE_LOCK:
        semaphore = _SEMAPHORES_BY_LOOP.get(loop)
        if semaphore is None:
            semaphore = asyncio.Semaphore(EMAIL_MAX_CONCURRENT)
            _SEMAPHORES_BY_LOOP[loop] = semaphore
        return semaphore


# envia correos en caso de fallar al enviar el correo original
async def _notify_failure_async(original_recipient, subject, error_message):
    notify_target = os.getenv("EMAIL_TO_RECIVE_ERROR")
    if not notify_target:
        return
    try:
        msg = _build_message(
            subject=f"Error al enviar correo a {original_recipient}",
            recipient=notify_target,
            html_message=f"""
            <html>
                <body>
                    <p><strong>Error al enviar correo a:</strong> {original_recipient}</p>
                    <p><strong>Asunto:</strong> {subject}</p>
                    <p><strong>Error:</strong></p>
                    <pre>{error_message}</pre>
                </body>
            </html>
            """,
        )
        await _send_message_async(msg, recipients=[notify_target])
    except Exception:
        logger.exception(
            "Fallo doble: no se pudo enviar correo original ni notificación de error recipient=%s",
            original_recipient,
        )

# orquestados de estructura de los correos
async def send_email(subject, html_message, recipient, id_long, cc=None):
    cc_recipients = cc or []
    envelope_recipients = [recipient, *cc_recipients]
    msg = _build_message(
        subject=subject,
        recipient=recipient,
        html_message=html_message,
        cc_recipients=cc_recipients,
    )
    total_attempts = EMAIL_MAX_RETRIES + 1

    async with _get_email_semaphore():
        for attempt in range(total_attempts):
            try:
                await _send_message_async(msg, recipients=envelope_recipients)
                return True
            except Exception:
                is_last_attempt = attempt == total_attempts - 1
                if is_last_attempt:
                    error_details = traceback.format_exc()
                    _mark_backup_pending(id_long)  # guardar en redis para el backup cuando se restablezca el servicio de correo
                    logger.exception("Error enviando correo participant_id=%s recipient=%s", id_long, recipient)
                    await _notify_failure_async(
                        original_recipient=recipient,
                        subject=subject,
                        error_message=error_details,
                    )
                    return False

                backoff_seconds = EMAIL_RETRY_BACKOFF_SECONDS * (2 ** attempt)
                if backoff_seconds > 0:
                    await asyncio.sleep(backoff_seconds)
