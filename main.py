from fastapi import FastAPI, Request
import asyncio
import xmltodict
from dotenv import load_dotenv
from mailer import send_email
from utils import is_duplicate
from utils import construir_url_consent
from utils import construir_url_part1, construir_url_part2, construir_url_part3, construir_url_phsample1, construir_url_follow1
from search_by_odk_api import buscar_correo_en_submissions, buscar_edad_en_submissions, buscar_datos_en_entidad_participantes
from fastapi import Request

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
        id_participant = parsed["data"]["participantes"].get("participante_id")
        short_id = parsed["data"]["participantes"].get("short_id")
        subject = "Proyecto Laura - Consentimiento informado"
        url_id = construir_url_consent(id_participant)
        message = f"""
            <p>Hola, gracias por tu interés en participar en el proyecto Laura.</p>
            
            <p>Ahora  que has completado el formulario de pre-registro, hemos generado un código de participante para tí</p>
            
            <p>{short_id}</p>
        
            <p>Este código permitirá proteger tu identidad, ya que podrás utilizarlo para identificarte en futuras interacciones dentro del proyecto sin dar tu nombre o apellido.</p>
        
            <p>Ahora continuemos con algo muy importante, el <strong>Consentimiento Informado</strong> <a href="https://drive.google.com/file/d/1rgvpfLpdQvESCBBQGlnZRyxP4wscF3X2/view?usp=sharing"><strong>(leer aquí)</strong></a>, para tu mayor comodidad también hemos realizado un video que lo explica <a href="https://drive.google.com/file/d/1Z_jL6Zjr-295Sd5mI5xPt9Nd5UP_-COI/view?usp=drive_link">(ver video aquí)</a>.</p>
        
            <p>Ya estás decidida a participar?, entonces ahora completa el formulario de consentimiento informado <a href={url_id}>(completar aquí)</a>, luego recibirás un correo con los enlaces de la encuesta</p>
        
            <p>Tu participación ayudará a que instituciones y tomadores de decisiones de todo el país conozcan los principales problemas de salud que aquejan a la mujer peruana.</p>
        
            
            <p>Atentamente,<br>
            Equipo del proyecto Laura</p>
            <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
        """
    elif form_id == "Laura2-piloto-encuesta-ic":
        participant_id = parsed["data"]["preamble"].get("part_id")  # <-- Aquí está el valor que vino vía prellenado
        consentimiento = parsed["data"]["consent"].get("Q0_accept_consent")
        print("🔎 participant_id (desde part_id):", participant_id)
        if consentimiento == "yes":
            email = buscar_correo_en_submissions(participant_id)
            edad = buscar_edad_en_submissions(participant_id)
            phone = parsed["data"]["preamble"].get("entity_phone")
            datos = buscar_datos_en_entidad_participantes(phone)
            short_id = datos.get("short_id")
            print("🔎 participant_id:", participant_id)
            subject = f"¡Gracias por completar el Consentimiento Informado del proyecto Laura!"
            url_p1 = construir_url_part1(participant_id, edad)
            url_p2 = construir_url_part2(participant_id)
            url_p3 = construir_url_part3(participant_id)
            message = f"""
                <p>Hola {short_id},</p>
    
                <p>Hemos recibido tu consentimiento informado para participar en este estudio. 🎉</p>
    
                <p>Ya podemos empezar con la <strong>Encuesta Nacional</strong>, la que hemos dividido en 3 bloques.</p>
                
                <p><strong>¡Importante!</strong>👀 Una vez que hayas iniciado cada bloque, el sistema solo guarda las respuestas cuando lo hayas terminado y <strong>enviado</strong>, por eso te pedimos que destines un momento del día para completarlo. Si sales antes de completarlo podrías perder lo que has avanzado.</p>
                
                
                <li>
                    Formulario 1 - Datos Generales: <a href={url_p1}>Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>. Ahora continúa con el bloque 2.
                </li>
                <li>
                    Formulario 2 - Salud Reproductiva y Mestrual: <a href={url_p2}>Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>. Ahora continúa con el bloque 3.
                </li>
                <li>
                    Formulario 3 - Salud Mental: <a href={url_p3}>Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>, ya terminaste!
                </li>
    
                <p>Muchas gracias por tu participación en el proyecto <strong>Laura</strong>. 🫶</p>
    
                <p>Atentamente,<br>
                Equipo del proyecto Laura</p>
    
                <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
            """
        else:
            email=None
            pass

    elif form_id == "Laura2-piloto-encuesta-p1" or form_id == "Laura2-piloto-encuesta-p2" or form_id == "Laura2-piloto-encuesta-p3":
        phone = parsed["data"]["preamble"].get("entity_phone")

        await asyncio.sleep(2)

        datos = buscar_datos_en_entidad_participantes(phone)
        short_id = datos.get("short_id")

        if datos.get("complete_p1")=='yes' and datos.get("complete_p2")=='yes' and datos.get("complete_p3")=='yes':
            email = datos.get("email")
            subject = f"¡Gracias por participar en el proyecto Laura!"
            message = f"""
                <p>Hola {short_id},</p>

                <p>Toda la información que nos enviaste ha sido registrada correctamente en nuestra base de datos, ya podemos empezar a investigar 🧑‍💻. ¡Ya estás formando parte de la historia de la salud femenina en el Perú!</p>

                <p>Estamos muy contentos de contar con tu participación en el Proyecto <strong>Laura</strong></p>

                <p>Si eres seleccionada para la siguiente fase del proyecto, una Trabajadora de Campo se pondrá en contacto contigo 😀.</p>

                <p>Atentamente,<br>
                Equipo del proyecto Laura</p>

                <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
            """
        else:
            email = None
            pass

    elif form_id == "Laura2-piloto-agendamiento":
        if parsed["data"].get("tipo_agendamiento") == 'scheduling' and parsed["data"].get("mes_visita") == 'm1' and parsed["data"].get("numero_visita") == '1':
            long_id = parsed["data"].get("part_id")
            urls1 = construir_url_phsample1(long_id)
            urlf1 = construir_url_follow1(long_id)
            email = parsed["data"].get("part_email")
            subject = f"¡Gracias por participar en el Seguimiento del proyecto LAURA!"
            message = f"""
                <p>Hola,</p>

                <p>Hemos agendado la primera visita de seguimiento. 🎉</p>
                
                <p> A continuacion podras iniciar los formulario.</p>
                
                <li>Formulario de Muestra de pH:
                    <a href={urls1}>
                        Acceder
                    </a>
                </li>
                
                <li>Formulario de Seguimiento:
                    <a href={urlf1}>
                        Acceder
                    </a>
                </li>

                <p><strong>¡Próximamente nos pondremos en contacto contigo!</strong> ☺️ Gracias a tus respuestas podremos dar a conocer a nivel nacional los principales problemas de salud que aquejan a la mujer peruana.</p>       

                <p>Muchas gracias por tu participación en el proyecto <strong>LAURA</strong>. 🫶</p>

                <p>Atentamente,<br>
                Equipo del proyecto LAURA</p>

                <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
            """
        else:
            email = None
            pass




    else:
        print(f"⚠️ Formulario no manejado: {form_id}")
        return {"status": "ignored", "message": f"Formulario {form_id} no procesado"}

    if email:
        await send_email(subject, message, email)
        print(f"✅ Email sent to {email} (ID: {instance_id})")
    else:
        print(f"⚠️ No se encontró correo válido para ID: {instance_id}")

    return {"status": "ok"}
