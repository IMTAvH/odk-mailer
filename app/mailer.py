import os
import aiosmtplib
from email.message import EmailMessage

async def send_email(subject, message, to_email):
    msg = EmailMessage()
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(message)

    await aiosmtplib.send(
        msg,
        hostname=os.getenv("EMAIL_HOST"),
        port=int(os.getenv("EMAIL_PORT", 587)),
        username=os.getenv("EMAIL_USER"),
        password=os.getenv("EMAIL_PASSWORD"),
        start_tls=True
    )
