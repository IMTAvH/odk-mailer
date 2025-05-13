import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

async def send_email(subject, html_message, recipient):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = os.getenv("EMAIL_FROM")
    msg["To"] = recipient

    part = MIMEText(html_message, "html")
    msg.attach(part)

    with smtplib.SMTP(os.getenv("EMAIL_HOST"), int(os.getenv("EMAIL_PORT"))) as server:
        server.starttls()
        server.login(os.getenv("EMAIL_USER"), os.getenv("EMAIL_PASSWORD"))
        server.send_message(msg)
