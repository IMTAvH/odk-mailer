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

    subject = "¡Gracias por participar en el proyecto LAURA!"
    message = """
Hola, muchas gracias por tu interés en el proyecto LAURA.

Ya que has completado el formulario de pre-registro, pasamos a la siguiente fase con el cuestionario de la *“Encuesta Nacional”* que comprende preguntas de datos generales y salud femenina.

También estás recibiendo el *consentimiento informado*, el cual te explica el porqué estamos realizando este estudio y tus derechos como participante. 
Te pedimos que leas este documento con atención. Al firmarlo, estarás autorizando a los investigadores principales a acceder a tus datos, los cuales serán manejados de manera *confidencial*. Recuerda que tu participación es completamente *voluntaria*.

A continuación encontrarás 3 enlaces donde encontrarás:

1. El consentimiento informado en versión escrita, son 4 páginas que deberás leer al detalle para poder participar:
https://drive.google.com/file/d/1rgvpfLpdQvESCBBQGlnZRyxP4wscF3X2/view?usp=sharing

2. También hemos preparado un video donde te explicamos el consentimiento informado:
(agrega aquí el link al video)

3. Enlace a la Encuesta Nacional:
(agrega aquí el link a la encuesta)

Gracias a tus respuestas podremos dar a conocer a nivel nacional los principales problemas de salud que aquejan a la mujer peruana.

— El equipo del proyecto LAURA
    """

    await send_email(subject, message, email)
    print(f"✅ Email sent to {email} (ID: {instance_id})")

    return {"status": "ok"}
