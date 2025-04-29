from fastapi import FastAPI, Request
import xmltodict
from dotenv import load_dotenv
from mailer import send_email
from utils import is_duplicate
import os

load_dotenv()

app = FastAPI()

@app.post("/hooks")
async def receive_webhook(req: Request):
    body = await req.json()
    raw_xml = body.get("data", {}).get("xml")

    if not raw_xml:
        return {"status": "error", "message": "No XML found"}

    parsed = xmltodict.parse(raw_xml)
    instance_id = parsed["data"]["meta"].get("instanceID")
    email = parsed["data"]["participantes"].get("correo")

    if not instance_id or not email:
        return {"status": "error", "message": "Missing instanceID or email"}

    if is_duplicate(instance_id):
        print(f"⚠️ Duplicate ignored: {instance_id}")
        return {"status": "duplicate", "message": "Already processed"}

    subject = "📬 New ODK Submission"
    message = f"A new form has been submitted.\n\nRecipient: {email}"

    await send_email(subject, message, email)
    print(f"✅ Email sent to {email} (ID: {instance_id})")

    return {"status": "ok"}
