import requests
import os
from search_by_odk_api import buscar_correo_en_submissions, buscar_edad_en_submissions, buscar_datos_en_entidad_participantes

processed_ids = set()

def is_duplicate(instance_id: str) -> bool:
    if instance_id in processed_ids:
        return True
    processed_ids.add(instance_id)
    return False

def construir_url_consent(valor_id):
    # valor_codificado = quote_plus(valor_id)  # para escapar caracteres especiales

    # Prueba
    # https://odkcentral.upch.edu.pe/-/single/ganT9xIuyBEkCmQ1mRY8cpeIWWzxhi8?st=YlRK8XkXCJsl3aX0uCcbawjukW8hZZewEd8hppK1H76bWMnzwuIyC9OcIgIwzdYs

    # Form consentimiento informado
    # https://odkcentral.upch.edu.pe/-/single/OPSyaTGS200C13abNqM1Pk8NLj3vAMT?st=DmtEtXeyGB!lZM1UXm98nYTvQSuzFDJE2NAscyeT5aTdeEHqe3eIP!2aVdrSmT9i

    formulario = {
            "form_id": "OPSyaTGS200C13abNqM1Pk8NLj3vAMT",
            "token": "DmtEtXeyGB!lZM1UXm98nYTvQSuzFDJE2NAscyeT5aTdeEHqe3eIP!2aVdrSmT9i"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&d[/data/preamble/part_id]={valor_id}"

def construir_url_part1(valor_id, edad):

    # Prueba
    # https://odkcentral.upch.edu.pe/-/single/oJaqbizarAl2a5ITzH2YsX2gjzETtZc?st=Ai6eTLM1bVT0MnYHivkTxXejfKiJLISTiexXD6hZF9rLr39ilDt6PS$n0zV4VbAG

    # https://odkcentral.upch.edu.pe/-/single/guiLDqa7lfyyWCBhv9k2AWvqqMuPni6?st=Zm78egptTVNqykyl2UY57k8RCh5n9l6YBilieqsg2Z0jtGuXrg2OcY$IPTwARukQ
    formulario = {
        "form_id": "guiLDqa7lfyyWCBhv9k2AWvqqMuPni6",
        "token": "Zm78egptTVNqykyl2UY57k8RCh5n9l6YBilieqsg2Z0jtGuXrg2OcY$IPTwARukQ",
        "part_id": "d[/data/preamble/part_id_2]",
        "age": "d[/data/general_data/Q1.3_age]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}&{formulario['age']}={edad}"

def construir_url_part2(valor_id):

    # Prueba
    # https://odkcentral.upch.edu.pe/-/single/fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX?st=l65vr7s7G80yoQAWHGnWXHOIWT!JeudSgB6CfxhOMIow4LK7rirRypW!mExW!0g2

    # https://odkcentral.upch.edu.pe/-/single/xZI6VypZiTI71JQ1YlzKBDsqG6ahzKv?st=UZk8rikW3mRRn3Ic7UidcfvWb3$uNeK0oZkIvi0JGUGSRufhyv1FzVzCt7BbFUkW
    formulario = {
        "form_id": "xZI6VypZiTI71JQ1YlzKBDsqG6ahzKv",
        "token": "UZk8rikW3mRRn3Ic7UidcfvWb3$uNeK0oZkIvi0JGUGSRufhyv1FzVzCt7BbFUkW",
        "part_id": "d[/data/preamble/part_id_3]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"

def construir_url_part3(valor_id):

    # Prueba
    # https://odkcentral.upch.edu.pe/-/single/vmngcom1ZaTITHFj5MHfJefN6Oevjk0?st=pNFemRmzNQmwZ8hYzdSo3ttz$jFNlIm9PKCcygRm9duzJOC6CJ3vIGvt1NI5dYm4

    # https://odkcentral.upch.edu.pe/-/single/CvCLsSXXVpoL537Bati0fXXrFIcj8MJ?st=Gp6hXKGnARJC7f4X4ybzXHQYt2VGIh!FPiss8N$MKLrXzZ69oHWmv8segsPNCp5u
    formulario = {
        "form_id": "CvCLsSXXVpoL537Bati0fXXrFIcj8MJ",
        "token": "Gp6hXKGnARJC7f4X4ybzXHQYt2VGIh!FPiss8N$MKLrXzZ69oHWmv8segsPNCp5u",
        "part_id": "d[/data/preamble/part_id_4]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"

def construir_url_phsample1(valor_id):
    # Prueba
    # https://odkcentral.upch.edu.pe/-/single/7jnsfd0erYNGJ5fATAtAjHUUvqBfc6R?st=N9Z5GAoSVhQ96S72hrfvQexqr7j4AC1ll3UyoBg51DOTBgvUrwv!GJJxDIQ5cbio

    formulario = {
        "form_id": "7jnsfd0erYNGJ5fATAtAjHUUvqBfc6R",
        "token": "N9Z5GAoSVhQ96S72hrfvQexqr7j4AC1ll3UyoBg51DOTBgvUrwv!GJJxDIQ5cbio",
        "part_id": "d[/data/part_id_5]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"

def construir_url_follow1(valor_id):
    # Prueba
    # https://odkcentral.upch.edu.pe/-/single/lxNHihgGR7WI8AGbzex7SSvgscT6JDD?st=LmbbLV8gJ99evOGLjjEgDOlUJWyQCQ0lLsdoFZbZkTYWfUFQcu5QdZHIFmYP24ul

    formulario = {
        "form_id": "lxNHihgGR7WI8AGbzex7SSvgscT6JDD",
        "token": "LmbbLV8gJ99evOGLjjEgDOlUJWyQCQ0lLsdoFZbZkTYWfUFQcu5QdZHIFmYP24ul",
        "part_id": "d[/data/welcome/part_id_6]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"

def construir_url_phsample2(valor_id):
    # Prueba
    # https://odkcentral.upch.edu.pe/-/single/AkvtvCaGcDuvrYXe5O4C6yBCQeYAhJN?st=Im4GDRjEBy$ejbBk$aaBSr$WEq71U4FgBhvLL02EGnx!gRkSjO6Vs5KRq9pE3G97

    formulario = {
        "form_id": "AkvtvCaGcDuvrYXe5O4C6yBCQeYAhJN",
        "token": "Im4GDRjEBy$ejbBk$aaBSr$WEq71U4FgBhvLL02EGnx!gRkSjO6Vs5KRq9pE3G97",
        "part_id": "d[/data/part_id_5]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"

def construir_url_follow2(valor_id):
    # Prueba
    # https://odkcentral.upch.edu.pe/-/single/VYZpXcx55EhBcwqmygc9CcvrfoG2C4k?st=JzVMoVwSprUgCR1Ev9RRrI5kMm5DqmPRTaQLi$2ARhNbbicev0haAeGmV4yc6IX0

    formulario = {
        "form_id": "VYZpXcx55EhBcwqmygc9CcvrfoG2C4k",
        "token": "JzVMoVwSprUgCR1Ev9RRrI5kMm5DqmPRTaQLi$2ARhNbbicev0haAeGmV4yc6IX0",
        "part_id": "d[/data/welcome/part_id_6]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"

#####################################
######## Template de correos ########
#####################################
def correo_consentimiento(parsed):
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

    return email, subject, message

def correo_encuesta_nac(participant_id, parsed):
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
                        Formulario 2 - Salud Reproductiva y Menstrual: <a href={url_p2}>Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>. Ahora continúa con el bloque 3.
                    </li>
                    <li>
                        Formulario 3 - Salud Mental: <a href={url_p3}>Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>, ya terminaste!
                    </li>

                    <p>Muchas gracias por tu participación en el proyecto <strong>Laura</strong>. 🫶</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
                """
    return email, subject, message

def correo_agradecimiento(datos):
    short_id = datos.get("short_id")
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
    return email, subject, message

def correo_asignacion_tc(parsed):
    email = parsed['data'].get('email')
    short_id = parsed['data'].get('long_id')[0:6]
    subject = f"Bienvenida a la siguiente fase del Proyecto Laura"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Bienvenida a la fase II del proyecto Laura 😄</p>

                    <p>¡Estamos muy contentas de contar con tu participación en el Proyecto Laura!</p>

                    <p>Recuerda que ya estás formando parte de la historia de la salud femenina en el Perú.</p>       

                    <p>El personal del estudio se pondrá en contacto contigo para entregarte tu <strong>“kit de bienvenida”</strong> donde encontrarás los materiales necesarios para donar tus muestras. Si tienes alguna duda puedes preguntarle a nuestro personal del estudio.</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
                """
    return email, subject, message

def correo_agendamiento_m1v1(parsed):
    long_id = parsed["data"].get("part_id")
    print(long_id)
    short_id = long_id[0:6]
    urls1 = construir_url_phsample1(long_id)
    urlf1 = construir_url_follow1(long_id)
    fecha = parsed["data"].get("fecha_visita_m1v1")
    email = parsed["data"].get("part_email")
    print(email)
    subject = f"Proyecto Laura - Bienvenida a la visita 1 de la fase II"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Muchas gracias por agendar la fecha de la <strong>primera visita</strong> del personal del estudio para la toma de tu <strong>primera muestra</strong> para la <strong>fase II</strong> del proyecto Laura 😄</p>

                    <p>¡Estamos muy contentas de contar con tu participación en el Proyecto Laura!</p>

                    <p>La fecha agendada es: <strong>{fecha}</strong></p>
                    
                    <p>Durante la visita del personal del estudio deberás abrir este correo para poder registrar el valor de tu pH vaginal usando este formulario (<a href={urls1}><strong>abrir</strong></a>) y para poder llenar tu primera encuesta de seguimiento (<a href={urlf1}><strong>abrir</strong></a>).</p>       

                    <p>Si tienes alguna duda puedes preguntarle a nuestro personal del estudio.</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
                """
    return email, subject, message


def correo_agendamiento_m1v2(parsed):
    long_id = parsed["data"].get("part_id")
    short_id = long_id[0:6]
    urls2 = construir_url_phsample2(long_id)
    urlf2 = construir_url_follow2(long_id)
    fecha = parsed["data"].get("fecha_visita_m1v2")
    email = parsed["data"].get("part_email")
    subject = f"Proyecto Laura - Bienvenida a la visita 2 de la fase II"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Muchas gracias por agendar la fecha de la <strong>segunda visita</strong> del personal del estudio para la toma de tu <strong>primera muestra</strong> para la <strong>fase II</strong> del proyecto Laura 😄</p>

                    <p>¡Estamos muy contentas de contar con tu participación en el Proyecto Laura!</p>

                    <p>La fecha agendada es: <strong>{fecha}</strong></p>

                    <p>Durante la visita del personal del estudio deberás abrir este correo para poder registrar el valor de tu pH vaginal usando este formulario (<a href={urls2}><strong>abrir</strong></a>) y para poder llenar la segunda encuesta de seguimiento (<a href={urlf2}><strong>abrir</strong></a>).</p>       

                    <p>Si tienes alguna duda puedes preguntarle a nuestro personal del estudio.</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
                """
    return email, subject, message