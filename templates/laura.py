LAURA_LOGO_SRC = "https://drive.usercontent.google.com/download?id=1M1Vbyx_CLMH1tNojWwp_lf0TQBhnsR6e&export"


def correo_encuesta_nac(parsed, next_form_url=None):
    email = parsed["data"]["participantes"].get("correo")
    short_id = parsed["data"]["participantes"].get("short_id")
    link_section = ""
    if next_form_url:
        link_section = f"""
                    <li>
                        Formulario Principal: <a href="{next_form_url}">Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>.
                    </li>
        """
    subject = "¡Gracias por completar el pre registro del proyecto Laura!"
    message = f"""

                    <p>Hola, gracias por tu interés en participar en el proyecto Laura.</p>

                    <p>Ahora  que has completado el formulario de pre-registro, hemos generado un código de participante para tí</p>

                    <p>{short_id}</p>

                    <p>Ya podemos empezar con la <strong>Encuesta Nacional</strong></p>

                    {link_section}

                    <p>Muchas gracias por tu participación en el proyecto <strong>Laura</strong>. 🫶</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="{LAURA_LOGO_SRC}" alt="Logo LAURA" width="150"/></p>
                """
    return email, subject, message


def correo_agradecimiento(parsed):
    short_id = parsed["data"]["preamble"]["entity_details"].get("short_id")
    subject = "¡Gracias por participar en el proyecto Laura!"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Toda la información que nos enviaste ha sido registrada correctamente en nuestra base de datos, ya podemos empezar a investigar 🧑‍💻. ¡Ya estás formando parte de la historia de la salud femenina en el Perú!</p>

                    <p>Estamos muy contentos de contar con tu participación en el Proyecto <strong>Laura</strong></p>

                    <p>Si eres seleccionada para la siguiente fase del proyecto, una Trabajadora de Campo se pondrá en contacto contigo 😀.</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="{LAURA_LOGO_SRC}" alt="Logo LAURA" width="150"/></p>
                """
    return subject, message

# laura
def correo_recordatorio(participante):
    short_id = participante["participante_id"][:6]
    reminder_url = participante.get("reminder_url")
    project_name = participante.get("project_name", "Proyecto")
    link_section = ""
    if reminder_url:
        link_section = f"""
                    <li>
                        Formulario Principal: <a href="{reminder_url}">Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>.
                    </li>
        """

    subject = f"Recordatorio - {project_name}"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Te recordamos que aún no has completado la encuesta del proyecto {project_name}. Tu participación es muy importante para nosotros.</p>

                    <p>Si tienes alguna duda o necesitas ayuda para completar la encuesta, no dudes en contactarnos.</p>
                    
                    {link_section}

                    <p>Atentamente,<br>
                    Equipo del proyecto {project_name}</p>

                    <p><img src="{LAURA_LOGO_SRC}" alt="Logo LAURA" width="150"/></p>
                """
    return subject, message


def correo_encuesta_nac_backup(
    participante,
    next_form_url=None,
    project_name="Laura",
    ):
    short_id = participante[:6]
    link_section = ""
    if next_form_url:
        link_section = f"""
                    <li>
                        Formulario Principal: <a href="{next_form_url}">Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>.
                    </li>
        """
    subject = f"¡Gracias por completar el pre registro del proyecto {project_name}!!"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Hola, gracias por tu interés en participar en el proyecto {project_name}.</p>

                    <p>Ahora  que has completado el formulario de pre-registro, hemos generado un código de participante para tí</p>
                    
                    {link_section}

                    <p>Muchas gracias por tu participación en el proyecto <strong>{project_name}</strong>. 🫶</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto {project_name}</p>

                    <p><img src="{LAURA_LOGO_SRC}" alt="Logo LAURA" width="150"/></p>
                """
    return subject, message


def correo_agradecimiento_backup(participante):
    short_id = participante[:6]
    subject = "¡Gracias por participar en el proyecto Laura!"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Toda la información que nos enviaste ha sido registrada correctamente en nuestra base de datos, ya podemos empezar a investigar 🧑‍💻. ¡Ya estás formando parte de la historia de la salud femenina en el Perú!</p>

                    <p>Estamos muy contentos de contar con tu participación en el Proyecto <strong>Laura</strong></p>

                    <p>Si eres seleccionada para la siguiente fase del proyecto, una Trabajadora de Campo se pondrá en contacto contigo 😀.</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="{LAURA_LOGO_SRC}" alt="Logo LAURA" width="150"/></p>
                """
    return subject, message
