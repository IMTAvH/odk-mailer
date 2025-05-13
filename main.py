from fastapi import FastAPI, Request
import xmltodict
from dotenv import load_dotenv
from mailer import send_email
from utils import is_duplicate
from search_by_odk_api import buscar_correo_en_submissions

load_dotenv()

app = FastAPI()

@app.post("/hooks")
async def receive_webhook(req: Request):
    body = await req.json()
    print("📩 Webhook recibido")
    print("📄 body:", body)
    raw_xml = body.get("data", {}).get("xml")

    if not raw_xml:
        return {"status": "error", "message": "No XML found"}

    parsed = xmltodict.parse(raw_xml)
    form_id = parsed["data"].get("@id")
    instance_id = parsed["data"]["meta"].get("instanceID")

    if is_duplicate(instance_id):
        print(f"⚠️ Duplicate ignored: {instance_id}")
        return {"status": "duplicate", "message": "Already processed"}

    if form_id == "Laura2-piloto-encuesta-preregistro":

        email = parsed["data"]["participantes"].get("correo")
        subject = "¡Gracias por participar en el proyecto LAURA!"
        message = """
            <p>Hola, muchas gracias por tu interés en el proyecto <strong>LAURA</strong>.</p>
        
            <p>Ya que has completado el formulario de pre-registro, pasamos a la siguiente fase con el cuestionario de la <strong>Encuesta Nacional</strong> que comprende preguntas de datos generales y salud femenina.</p>
        
            <p>También estás recibiendo el <strong>consentimiento informado</strong>, el cual te explica el porqué estamos realizando este estudio y tus derechos como participante. 🫡</p>
        
            <p>Te pedimos que leas este documento con atención. Al firmarlo, estarás autorizando a los investigadores principales a acceder a tus datos, los cuales serán manejados de manera <strong>confidencial</strong>. Recuerda que tu participación es completamente <strong>voluntaria</strong>.</p>
        
            <p>👉 A continuación encontrarás 3 enlaces:</p>
        
            <ol>
                <li>El consentimiento informado en versión escrita, son 4 páginas que deberás leer al detalle para poder participar: 
                    <a href="https://drive.google.com/file/d/1rgvpfLpdQvESCBBQGlnZRyxP4wscF3X2/view?usp=sharing">
                        Leer documento PDF
                    </a>
                </li>
                <li>También hemos preparado un video donde te explicamos el consentimiento informado:
                    <a href="https://www.youtube.com/watch?v=video_demo">
                        Ver video
                    </a>
                </li>
                <li>Encuesta Nacional:
                    <a href="https://odkcentral.upch.edu.pe/-/single/b77d299342bebf196c723f10284d2a963d2251c08eb161f2595d73055cefa2cb?st=J$auHziEkSa3LF2haS9JIWi2eeyFc7nJFhgLKO$JnpZxr$2b0fd8eC!N2sHf$Ow2">
                        Acceder a la encuesta
                    </a>
                </li>
            </ol>
        
            <p><strong>¡Importante!</strong>👀 Esta encuesta Nacional te tomará aproximadamente <strong>50 minutos</strong>, por favor te pedimos que encuentres un momento del día para que puedas responder con calma.</p>
            
            <p><strong>¡Próximamente nos pondremos en contacto contigo!</strong> ☺️ Gracias a tus respuestas podremos dar a conocer a nivel nacional los principales problemas de salud que aquejan a la mujer peruana.</p>       
            
            <p>Atentamente,</p>
            <p><img src="https://drive.google.com/file/d/109KJ3wBlPtuv5uc1QsM3igm61v6OO00O/view?usp=sharing" alt="Logo LAURA" width="150"/></p>
            """
    elif form_id == "Laura2-piloto-encuesta-p1":
        participant_id = parsed["data"]["general_data"].get("Q1.2_participant_id")
        email = buscar_correo_en_submissions(participant_id)
        print("🔎 participant_id:", participant_id)
        subject = f"Gracias por tu envío desde el formulario {form_id}"
        message = "Tu informacion ha sido registrada."

    if email:
        await send_email(subject, message, email)
        print(f"✅ Email sent to {email} (ID: {instance_id})")
    else:
        print(f"⚠️ No se encontró correo válido para ID: {instance_id}")

    return {"status": "ok"}
