import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import traceback

def notify_failure(original_recipient, subject, error_message):
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"❌ Error al enviar correo a {original_recipient}"
        msg["From"] = os.getenv("EMAIL_FROM")
        msg["To"] = "renato.cava@upch.pe"

        body = f"""
        <html>
            <body>
                <p><strong>Error al enviar correo a:</strong> {original_recipient}</p>
                <p><strong>Asunto:</strong> {subject}</p>
                <p><strong>Error:</strong></p>
                <pre>{error_message}</pre>
            </body>
        </html>
        """

        part = MIMEText(body, "html")
        msg.attach(part)

        with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)
    except Exception as inner_error:
        # Último recurso: registrar en consola
        print("🔴 Fallo doble: No se pudo enviar ni el correo original ni la notificación de error.")
        print(traceback.format_exc())

async def send_email(subject, html_message, recipient):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = recipient

    part = MIMEText(html_message, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
            server.starttls()
            server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
            server.send_message(msg)
    except Exception as e:
        # Si falla, construye mensaje de error y mándalo a renato.cava@upch.pe
        error_details = traceback.format_exc()
        notify_failure(
            original_recipient=recipient,
            subject=subject,
            error_message=error_details
        )
