import os
processed_ids = set()

def is_duplicate(instance_id: str) -> bool:
    if instance_id in processed_ids:
        return True
    processed_ids.add(instance_id)
    return False

    
def construir_url_encuesta_Nacional_Completa(valor_id):
    return f"{os.getenv('URL_ENCUESTA_NACIONAL')}&d[/data/preamble/part_id]={valor_id}"


#####################################
######## Template de correos ########
#####################################

def correo_encuesta_nac(parsed):

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

def correo_recordatorio(participante):
    short_id = participante['participante_id'][:6]
    url_enc = construir_url_encuesta_Nacional_Completa(participante['participante_id'])
    subject = f"Recordatorio - Proyecto Laura"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Te recordamos que aún no has completado la encuesta nacional del proyecto Laura. Tu participación es muy importante para nosotros y para la salud de las mujeres en el Perú.</p>

                    <p>Si tienes alguna duda o necesitas ayuda para completar la encuesta, no dudes en contactarnos.</p>
                    
                    <li>
                        Formulario Principal: <a href={url_enc}>Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>.
                    </li>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
                """
    return subject, message


def correo_encuesta_nac_backup(participante):
    short_id = participante[:6]
    url_enc = construir_url_encuesta_Nacional_Completa(participante)
    subject = f"¡Gracias por completar el pre registro del proyecto Laura!!"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Hola, gracias por tu interés en participar en el proyecto Laura.</p>

                    <p>Ahora  que has completado el formulario de pre-registro, hemos generado un código de participante para tí</p>
                    
                    <li>
                        Formulario Principal: <a href={url_enc}>Acceder</a> - Llena tus respuestas y presiona <strong>enviar</strong>.
                    </li>

                    <p>Muchas gracias por tu participación en el proyecto <strong>Laura</strong>. 🫶</p>

                    <p>Atentamente,<br>
                    Equipo del proyecto Laura</p>

                    <p><img src="https://drive.google.com/uc?export=view&id=109KJ3wBlPtuv5uc1QsM3igm61v6OO00O" alt="Logo LAURA" width="150"/></p>
                """
    return subject, message

def correo_agradecimiento_backup(participante: str):
    short_id = participante[:6]
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

#### verificacion en redis y actualizacion rapida del email

EMAIL_CAS_LUA = """
-- KEYS[1] = key del participante (hash)
-- ARGV[1] = nuevo email normalizado
local key = KEYS[1]
local new_email = ARGV[1]

-- 0 = no existe key
if redis.call('EXISTS', key) == 0 then
  return 0
end

-- 1 = email igual, no hacer nada
local current = redis.call('HGET', key, 'email')
if current == new_email then
  return 1
end

-- 2 = email cambiado, Actualiza email
redis.call('HSET', key, 'email', new_email)
return 2
"""
