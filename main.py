from fastapi import FastAPI, Request
import xmltodict
from dotenv import load_dotenv
from mailer import send_email
from utils import is_duplicate
from utils import construir_url_consent
from utils import construir_url_part1, construir_url_part2, construir_url_part3
from search_by_odk_api import buscar_correo_en_submissions, buscar_edad_en_submissions
from fastapi import Request

# from fastapi import HTTPException
# from fastapi.responses import RedirectResponse
# from urllib.parse import quote

load_dotenv()

app = FastAPI()


# @app.get("/next")
# def next(part_id: str, form: str):
#
#     if not part_id:
#         raise HTTPException(status_code=422, detail="Falta part_id")
#
#
#     # {
#     #     "form_id": "v3NUCyLIXypt4ocz0YbKg5uoxRY5BYD",
#     #     "token": "qXltW8xMvAIRils99XG9IUYvoNtRz53xPcB9V2fEiz6kbQtFOV8swVwZze3x$4EL",
#     #     "part_id": "d[/data/general_health/part_id_5]"
#     # },
#     # Form Part 4
#     # https://odkcentral.upch.edu.pe/-/single/v3NUCyLIXypt4ocz0YbKg5uoxRY5BYD?st=qXltW8xMvAIRils99XG9IUYvoNtRz53xPcB9V2fEiz6kbQtFOV8swVwZze3x$4EL
#
#     # {
#     #     "form_id": "vmngcom1ZaTITHFj5MHfJefN6Oevjk0",
#     #     "token": "xU2nudC!h$gAzcDoe5TcqK5pz4RQfAUN0HqtyHRrEW1oy4mcvfz$rRBsNnQzW0Mn",
#     #     "part_id": "d[/data/personal_hygiene/part_id_4]"
#     # },
#     # Form Part 3
#     # https://odkcentral.upch.edu.pe/-/single/vmngcom1ZaTITHFj5MHfJefN6Oevjk0?st=xU2nudC!h$gAzcDoe5TcqK5pz4RQfAUN0HqtyHRrEW1oy4mcvfz$rRBsNnQzW0Mn
#
#     # {
#     #     "form_id": "fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX",
#     #     "token": "d4YCxBKvsx$tkKOWB6OD0RPijaxIAc1ktxG58KvPKFaQYTRKWNsQUYjTO$aCJW9f",
#     #     "part_id": "d[/data/End/part_id_3]"
#     # },
#     # Form Part 2
#     # https://odkcentral.upch.edu.pe/-/single/fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX?st=d4YCxBKvsx$tkKOWB6OD0RPijaxIAc1ktxG58KvPKFaQYTRKWNsQUYjTO$aCJW9f
#
#
#     # Definir lógica por formulario que se pide
#     if form == "f2":
#         form_id = "fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX"
#         token = "d4YCxBKvsx$tkKOWB6OD0RPijaxIAc1ktxG58KvPKFaQYTRKWNsQUYjTO$aCJW9f"
#         field = "d[/data/End/part_id_3]",
#         next_form = "f3"
#     elif form == "f3":
#         form_id = "vmngcom1ZaTITHFj5MHfJefN6Oevjk0"
#         token = "xU2nudC!h$gAzcDoe5TcqK5pz4RQfAUN0HqtyHRrEW1oy4mcvfz$rRBsNnQzW0Mn"
#         field = "d[/data/personal_hygiene/part_id_4]",
#         next_form = "f4"
#     elif form == "f4":
#         form_id = "v3NUCyLIXypt4ocz0YbKg5uoxRY5BYD"
#         token = "qXltW8xMvAIRils99XG9IUYvoNtRz53xPcB9V2fEiz6kbQtFOV8swVwZze3x$4EL"
#         field = "d[/data/general_health/part_id_5]",
#         next_form = "f5"
#     else:
#         raise HTTPException(status_code=404, detail="Formulario desconocido")
#
#     base = "https://odkcentral.upch.edu.pe/-/single"
#     url = f"{base}/{form_id}?st={token}&{quote(field)}={quote(part_id)}"
#
#     if next_form:
#         # Crear returnUrl para el siguiente paso
#         return_url = f"https://odkcentral.upch.edu.pe:4000/next?part_id={quote(part_id)}&form={next_form}"
#         url += f"&returnUrl={quote(return_url, safe='')}"
#
#     return RedirectResponse(url)


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
        id_participant = parsed["data"]["participantes"].get("participante_id")
        short_id = parsed["data"]["participantes"].get("short_id")
        subject = "¡Gracias por participar en el proyecto LAURA!"
        url_id = construir_url_consent(id_participant)
        message = f"""
            <p>Hola, muchas gracias por tu interés en el proyecto <strong>LAURA</strong>.</p>
            
            <p>Tu codigo de participante es: {short_id}</p>
        
            <p>Ya que has completado el formulario de pre-registro, pasamos a la siguiente fase con el cuestionario del <strong>Consentiemiento Informado</strong></p>
        
            <p>El Consentimiento Informado te explica el porqué estamos realizando este estudio y tus derechos como participante. 🫡</p>
        
            <p>Te pedimos que leas el documento adjunto con atención y luego completes el formulario de consentimiento informado. Al firmarlo, estarás autorizando a los investigadores principales a acceder a tus datos, los cuales serán manejados de manera <strong>confidencial</strong>. Recuerda que tu participación es completamente <strong>voluntaria</strong>.</p>
        
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
                <li>Formulario de consentimiento informado:
                    <a href={url_id}>
                        Acceder
                    </a>
                </li>
            </ol>
            
            <p>Atentamente,<br>
            Equipo del proyecto LAURA</p>
            <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
        """
    elif form_id == "Laura2-piloto-encuesta-ic":
        participant_id = parsed["data"].get("part_id")  # <-- Aquí está el valor que vino vía prellenado
        print("🔎 participant_id (desde part_id):", participant_id)
        email = buscar_correo_en_submissions(participant_id)
        edad = buscar_edad_en_submissions(participant_id)
        short_id = parsed["data"]["participantes"].get("short_id")
        print("🔎 participant_id:", participant_id)
        subject = f"¡Gracias por completar el Consentimiento Informado del proyecto LAURA!"
        url_p1 = construir_url_part1(participant_id, edad)
        url_p2 = construir_url_part2(participant_id)
        url_p3 = construir_url_part3(participant_id)
        message = f"""
            <p>Hola,</p>

            <p>Hemos recibido correctamente tu consentimiento informado. 🎉</p>

            <p>Tu información ha sido registrada en nuestra base de datos de forma <strong>segura y confidencial</strong>.</p>
            
            <p>Recordar que tu codigo de participante es: {short_id}</p>
            
            <p> A continuacion podras iniciar la Encuesta Nacional </p>
            
            <li>Formulario de Datos Generales:
                <a href={url_p1}>
                    Acceder
                </a>
            </li>
            <li>Formulario de Salud Reproductiva y Mestrual:
                <a href={url_p2}>
                    Acceder
                </a>
            </li>
            <li>Formulario de Salud Mental:
                <a href={url_p3}>
                    Acceder
                </a>
            </li>

           <p><strong>¡Importante!</strong>👀 Esta encuesta Nacional te tomará aproximadamente <strong>50 minutos</strong>, por favor te pedimos que encuentres un momento del día para que puedas responder con calma.</p>
            
            <p><strong>¡Próximamente nos pondremos en contacto contigo!</strong> ☺️ Gracias a tus respuestas podremos dar a conocer a nivel nacional los principales problemas de salud que aquejan a la mujer peruana.</p>       

            <p>Muchas gracias por tu participación en el proyecto <strong>LAURA</strong>. 🫶</p>

            <p>Atentamente,<br>
            Equipo del proyecto LAURA</p>

            <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
        """

    else:
        print(f"⚠️ Formulario no manejado: {form_id}")
        return {"status": "ignored", "message": f"Formulario {form_id} no procesado"}

    if email:
        await send_email(subject, message, email)
        print(f"✅ Email sent to {email} (ID: {instance_id})")
    else:
        print(f"⚠️ No se encontró correo válido para ID: {instance_id}")

    return {"status": "ok"}
