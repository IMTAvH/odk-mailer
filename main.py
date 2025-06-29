from fastapi import FastAPI
from fastapi import Request
import xmltodict
from dotenv import load_dotenv
from mailer import send_email
from utils import is_duplicate, correo_consentimiento, correo_encuesta_nac, correo_agradecimiento, correo_asignacion_tc, correo_agendamiento_m1v1, correo_agendamiento_m1v2, correo_agendamiento_m1v3, correo_agendamiento_m2v1, correo_agendamiento_m2v2, correo_agendamiento_m2v3
from search_by_odk_api import buscar_submissions_en_p1, buscar_submissions_en_p2, buscar_submissions_en_p3

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
        email, subject, message = correo_consentimiento(parsed)

    elif form_id == "Laura2-piloto-encuesta-ic":
        participant_id = parsed["data"]["preamble"].get("part_id")  # <-- Aquí está el valor que vino vía prellenado
        consentimiento = parsed["data"]["consent"].get("Q0_accept_consent")
        print("🔎 participant_id (desde part_id):", participant_id)
        if consentimiento == "yes":
            email, subject, message = correo_encuesta_nac(participant_id, parsed)

        else:
            print("Participante no acepto el consentimiento informado")
            email=None

    elif form_id == "Laura2-piloto-encuesta-p1":
        # phone = parsed["data"]["preamble"].get("entity_phone")
        # datos = buscar_datos_en_entidad_participantes(phone)
        participant_id = parsed["data"]["preamble"].get("part_id_2")
        complete_p2 = buscar_submissions_en_p2(participant_id)
        complete_p3 = buscar_submissions_en_p3(participant_id)
        if complete_p2=='yes' and complete_p3=='yes':
            email, subject, message = correo_agradecimiento(parsed)

        else:
            email = None
            pass

    elif form_id == "Laura2-piloto-encuesta-p2":
        # phone = parsed["data"]["preamble"].get("entity_phone")
        # datos = buscar_datos_en_entidad_participantes(phone)
        participant_id = parsed["data"]["preamble"].get("part_id_3")
        complete_p1 = buscar_submissions_en_p1(participant_id)
        complete_p3 = buscar_submissions_en_p3(participant_id)
        if complete_p1=='yes' and complete_p3=='yes':
            email, subject, message = correo_agradecimiento(parsed)

        else:
            email = None
            pass

    elif form_id == "Laura2-piloto-encuesta-p3":
        # phone = parsed["data"]["preamble"].get("entity_phone")
        # datos = buscar_datos_en_entidad_participantes(phone)
        participant_id = parsed["data"]["preamble"].get("part_id_4")
        complete_p1 = buscar_submissions_en_p1(participant_id)
        complete_p2 = buscar_submissions_en_p2(participant_id)
        if complete_p1=='yes' and complete_p2=='yes':
            email, subject, message = correo_agradecimiento(parsed)

        else:
            email = None
            pass

    elif form_id == "Laura2-piloto-asignacion":
        email, subject, message = correo_asignacion_tc(parsed)

    elif form_id == "Laura2-piloto-agendamiento":
        if parsed["data"].get("mes_visita") == 'm1' and parsed["data"].get("numero_visita") == 'v1':
            print(parsed)
            email, subject, message = correo_agendamiento_m1v1(parsed)

        elif parsed["data"].get("mes_visita") == 'm1' and parsed["data"].get("numero_visita") == 'v2':
            email, subject, message = correo_agendamiento_m1v2(parsed)

        elif parsed["data"].get("mes_visita") == 'm1' and parsed["data"].get("numero_visita") == 'v3':
            email, subject, message = correo_agendamiento_m1v3(parsed)

        elif parsed["data"].get("mes_visita") == 'm2' and parsed["data"].get("numero_visita") == 'v1':
            email, subject, message = correo_agendamiento_m2v1(parsed)

        elif parsed["data"].get("mes_visita") == 'm2' and parsed["data"].get("numero_visita") == 'v2':
            email, subject, message = correo_agendamiento_m2v2(parsed)

        elif parsed["data"].get("mes_visita") == 'm2' and parsed["data"].get("numero_visita") == 'v3':
            email, subject, message = correo_agendamiento_m2v3(parsed)

        else:
            email = None
            pass

    else:
        print(f"⚠️ Formulario no manejado: {form_id}")
        return {"status": "ignored", "message": f"Formulario {form_id} no procesado"}

    if email:
        print(f"✅ Enviando correo a {email} (ID: {instance_id})")
        await send_email(subject=subject, html_message=message, recipient=email)
        print(f"✅ Correo enviado a {email}")
    else:
        print(f"⚠️ No se encontró correo para ID: {instance_id}")

    return {"status": "ok"}
