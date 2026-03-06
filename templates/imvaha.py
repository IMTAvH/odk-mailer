UNAP_LOGO_SRC = "https://drive.usercontent.google.com/download?id=1FpgBnTYxP4ns541uf5Uga1N2Dnqnhnhc&export"
IMVAHA_LOGO_SRC = "https://drive.usercontent.google.com/download?id=1aRBPCRY7bOcSyJsA3EV-kEX4ExgAir00&export"


def _logos_block():
    return f"""
                    <table role="presentation" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                            <td style="padding-right: 12px;">
                                <img src="{UNAP_LOGO_SRC}" alt="Logo UNAP" width="120"/>
                            </td>
                            <td>
                                <img src="{IMVAHA_LOGO_SRC}" alt="Logo IMVAHA" width="120"/>
                            </td>
                        </tr>
                    </table>
    """


def correo_preregistro_imvaha(
    email,
    short_id,
    next_form_url=None,
):
    link_section = ""
    if next_form_url:
        link_section = f"""
                    <p>Si corresponde, puedes continuar aquí: <a href="{next_form_url}">Acceder</a>.</p>
        """
    logos = _logos_block()
    subject = "Bienvenida a IMVAHA Perú - Tu código de participante"
    message = f"""
                    <p>Hola,</p>

                    <p>¡Bienvenida a IMVAHA Perú! Gracias por tu interés y por completar el pre-registro.</p>

                    <p>Tu código de participante es: <strong>{short_id or 'sin-codigo'}</strong></p>
                    <p>Te pedimos que lo guardes (lo necesitaremos para tu participación y para proteger tu privacidad).</p>

                    <p>De acuerdo con las opciones de participación que elegiste durante la pre-inscripción,
                    te contactaremos próximamente para contarte los siguientes pasos del estudio.</p>

                    {link_section}

                    <p>Si tienes cualquier duda, puedes escribirnos a <strong>imvaha@unapiquitos.edu.pe</strong>
                    o contactarnos por WhatsApp <strong>904 133 591</strong>.</p>

                    <p>Para novedades del proyecto, síguenos en Instagram <strong>@imvaha_unapiquitos</strong> y Facebook <strong>imvahaunapiquitos</strong>.</p>

                    <p>Un saludo,<br>
                    Equipo IMVAHA Perú</p>

                    <p><strong>Hablar de menstruación es hablar de derechos, salud y bienestar</strong><br>
                    <em>¡Cada experiencia cuenta, cada voz cuenta!</em></p>

                    <p>Si no realizaste este pre-registro, puedes ignorar este mensaje.</p>

                    {logos}
                """
    return email, subject, message


def correo_preregistro_backup_imvaha(
    participante,
    next_form_url=None,
    project_name=None,
):
    short_id = participante[:6] if participante else "sin-codigo"
    link_section = ""
    if next_form_url:
        link_section = f"""
                    <p>Si corresponde, puedes continuar aquí: <a href="{next_form_url}">Acceder</a>.</p>
        """
    logos = _logos_block()
    subject = "Bienvenida a IMVAHA Perú - Tu código de participante"
    message = f"""
                    <p>Hola,</p>

                    <p>¡Bienvenida a IMVAHA Perú! Gracias por tu interés y por completar el pre-registro.</p>
                    <p>Tu código de participante es: <strong>{short_id}</strong></p>
                    <p>Te pedimos que lo guardes (lo necesitaremos para tu participación y para proteger tu privacidad).</p>
                    <p>De acuerdo con las opciones de participación que elegiste durante la pre-inscripción,
                    te contactaremos próximamente para contarte los siguientes pasos del estudio.</p>
                    {link_section}

                    <p>Si tienes cualquier duda, puedes escribirnos a <strong>imvaha@unapiquitos.edu.pe</strong>
                    o contactarnos por WhatsApp <strong>904 133 591</strong>.</p>

                    <p>Para novedades del proyecto, síguenos en Instagram <strong>@imvaha_unapiquitos</strong> y Facebook <strong>imvahaunapiquitos</strong>.</p>

                    <p>Un saludo,<br>
                    Equipo IMVAHA Perú</p>

                    <p><strong>Hablar de menstruación es hablar de derechos, salud y bienestar</strong><br>
                    <em>¡Cada experiencia cuenta, cada voz cuenta!</em></p>

                    <p>Si no realizaste este pre-registro, puedes ignorar este mensaje.</p>

                    {logos}
                """
    return subject, message


def correo_recordatorio_imvaha(participante):
    short_id = participante["participante_id"][:6]
    reminder_url = participante.get("reminder_url")
    project_name = participante.get("project_name", "IMVAHA")
    link_section = ""
    if reminder_url:
        link_section = f"""
                    <p>Formulario principal: <a href="{reminder_url}">Acceder</a>.</p>
        """
    logos = _logos_block()
    subject = f"Recordatorio - {project_name}"
    message = f"""
                    <p>Hola {short_id},</p>

                    <p>Tu participacion es importante para nosotros.</p>

                    {link_section}

                    <p>Si tienes dudas, puedes escribirnos a <strong>imvaha@unapiquitos.edu.pe</strong>
                    o contactarnos por WhatsApp <strong>904 133 591</strong>.</p>

                    <p>Un saludo,<br>
                    Equipo IMVAHA Peru</p>

                    {logos}
                """
    return subject, message
