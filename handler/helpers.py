def _get_nested(payload, *keys):
    current = payload
    for key in keys:
        if not isinstance(current, dict):
            return None
        current = current.get(key)
        if current is None:
            return None
    return current


def _save_participant(
    redis_client,
    participant_id,
    email,
    estado,
    project_id,
    project_name=None,
    next_form_url=None,
    reminder_enabled=None,
    reminder_url=None,
):
    participante_data = {
        "email": email,
        "estado": estado,
        "backup": "0",
    }
    if project_id:
        participante_data["project_id"] = project_id
    if project_name:
        participante_data["project_name"] = project_name
    if next_form_url:
        participante_data["next_form_url"] = next_form_url
    if reminder_enabled is not None:
        participante_data["reminder_enabled"] = "1" if bool(reminder_enabled) else "0"
    if reminder_url:
        participante_data["reminder_url"] = reminder_url

    redis_client.hset(f"participante:{participant_id}", mapping=participante_data)
    redis_client.expire(f"participante:{participant_id}", 3888000)
