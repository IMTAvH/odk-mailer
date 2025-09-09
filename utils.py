processed_ids = set()

def is_duplicate(instance_id: str) -> bool:
    if instance_id in processed_ids:
        return True
    processed_ids.add(instance_id)
    return False

'''
def construir_url_preregistro(valor_id):
    return f"https://odk4.jellbru.xyz/f/GEvyfPxt5FbnNDeXQhbfKBMY5kH59el?st=TuUMvQ6vSUtyfSyo2RhMVj0T!F1seywiqNto77VjOIJArUlrqOiOfds9UFE1Qnxl&d[/data/preamble/part_id]={valor_id}"

def construir_url_consent(valor_id):
    return f"https://odk4.jellbru.xyz/f/WXllZxnco0cb7nM5aZ6vIxMfhxZyF0q?st=E2tH6V8XqTWsp9XtQqSE0lFyI8MG38CoQVSkiTdcywzqa3ibvD4fhS5E5$RMM0mX&d[/data/preamble/part_id]={valor_id}"
'''
    
def construir_url_encuesta_Nacional_Completa(valor_id):
    return f"https://odk4.jellbru.xyz/f/7c8uSPg5izDihYBtol4GGn2eRphkImD?st=Ba4m6dV01NDs2wwze1nzNphV9fYT3J0zFgC5clHHeVYZBn2guomnAimYZGDdsC3G&d[/data/preamble/part_id]={valor_id}"

'''
def construir_url_part1(valor_id):
    return f"https://odk4.jellbru.xyz/f/955ZV2HoN2cizrNF3O5x1RiLqIhsm61?st=th!veiIAv$TyNpcpkGBwP$cg1Ztvl1GWqXl62pjNLHMht1N8HxbyISeamF9CaUUo&d[/data/preamble/part_id_2]={valor_id}"

def construir_url_part2(valor_id):
    return f"https://odk4.jellbru.xyz/f/bbbp6esbv53vnvA794y79duCN5mDRSI?st=u8QSpGo9wkEUiZ3ezo!mzJhDJCSABfY!!tWV8Nxp!rHNa4GssyvvF67Nivq2fzdl&d[/data/preamble/part_id_3]={valor_id}"

def construir_url_part3(valor_id):
    return f"https://odk4.jellbru.xyz/f/JmecdlJqGfThdu8C2YoHd3dPFUoKAnV?st=sf11SHymo7kqK6jHAakAypIYkFPJ8rCR95NGBKaXChnP224W15FQTD7ok!oi7Lf1&d[/data/preamble/part_id_4]={valor_id}"

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

'''

#####################################
######## Template de correos ########
#####################################
'''
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
'''
    
def correo_encuesta_nac(parsed):
    # email = buscar_correo_en_submissions(participant_id)
    # edad = buscar_edad_en_submissions(participant_id)
    #email = parsed["data"].get("entity_email")
    #short_id = parsed["data"].get("entity_short_id")
    # phone = parsed["data"]["preamble"].get("entity_phone")
    # datos = buscar_datos_en_entidad_participantes(phone)
    # short_id = datos.get("short_id")
    #url_enc = construir_url_part1(participant_id)
    #url_p2 = construir_url_part2(participant_id)
    #url_p3 = construir_url_part3(participant_id)
    # print("🔎 participant_id:", participant_id)

    email = parsed["data"]["participantes"].get("correo")
    id_participant = parsed["data"]["participantes"].get("participante_id")
    short_id = parsed["data"]["participantes"].get("short_id")
    url_enc = construir_url_encuesta_Nacional_Completa(id_participant)
    subject = f"¡Gracias por completar el pre registro del proyecto Laura!"
    message = f"""

                    <p>Hola, gracias por tu interés en participar en el proyecto Laura.</p>

                    <p>Ahora  que has completado el formulario de pre-registro, hemos generado un código de participante para tí</p>

                    <p>{short_id}</p>

                    <p>Ya podemos empezar con la <strong>Encuesta Nacional</strong></p>

                    <li>
                        Formulario Principal: <a href={url_enc}>Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>.
                    </li>

                    <p>Muchas gracias por tu participación en el proyecto <strong>Laura</strong>. 🫶</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
                """
    return email, subject, message

def correo_agradecimiento(parsed):
    # short_id = datos.get("short_id")
    short_id = parsed["data"]["preamble"]["entity_details"].get("short_id")
    # email = datos.get("email")
    #email = parsed["data"]["preamble"].get("entity_email")
    #email = buscar_correo_en_submissions(participant_id)
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
    return subject, message

'''

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

def correo_agendamiento_m1v3(parsed):
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

def correo_agendamiento_m2v1(parsed):
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

def correo_agendamiento_m2v2(parsed):
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

def correo_agendamiento_m2v3(parsed):
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

'''