import json
from pathlib import Path


DEFAULT_FORMS_REGISTRY_PATH = Path(__file__).resolve().parent / "forms_registry.json"


def _resolve_url(url):
    return (url or "").strip() or None


def _as_bool(value, default=False):
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


# Normaliza cualquier valor de config a una lista de strings no vacíos.
# Acepta None, string único o lista.
def _to_list(value):
    if value is None:
        return []
    if isinstance(value, str):
        item = value.strip()
        return [item] if item else []
    if isinstance(value, list):
        result = []
        for item in value:
            text = str(item).strip()
            if text:
                result.append(text)
        return result
    return []


# Combina CC de proyecto y de ruta, y elimina duplicados sin importar mayúsculas.
def resolve_cc(route_config=None, project_config=None):
    route_config = route_config or {}
    project_config = project_config or {}
    combined = _to_list(project_config.get("cc")) + _to_list(route_config.get("cc"))
    seen = set()
    out = []
    for email in combined:
        key = email.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(email)
    return out


def resolve_next_form_url(route_config):
    route_config = route_config or {}
    return _resolve_url(route_config.get("next_form_url"))


def resolve_route_reminder_url(route_config):
    route_config = route_config or {}
    return _resolve_url(route_config.get("reminder_url"))


def resolve_route_reminder_enabled(route_config):
    route_config = route_config or {}
    return _as_bool(route_config.get("reminder_enabled"), default=False)


def resolve_reminder_url(project_config):
    project_config = project_config or {}
    return _resolve_url(project_config.get("reminder_url"))


def resolve_reminder_enabled(project_config):
    project_config = project_config or {}
    return _as_bool(project_config.get("reminder_enabled"), default=False)


def load_form_routes(path=DEFAULT_FORMS_REGISTRY_PATH):
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)

    routes = {}
    for entry in payload.get("routes", []):
        project_id = str(entry.get("project_id", "")).strip()
        form_id = str(entry.get("form_id", "")).strip()
        handler_name = str(entry.get("handler", "")).strip()

        if not project_id or not form_id or not handler_name:
            continue

        route_entry = dict(entry)
        route_entry["project_id"] = project_id
        route_entry["form_id"] = form_id
        route_entry["handler"] = handler_name
        routes[(project_id, form_id)] = route_entry

    projects = {}
    for entry in payload.get("projects", []):
        project_id = str(entry.get("project_id", "")).strip()
        if not project_id:
            continue
        project_entry = dict(entry)
        project_entry["project_id"] = project_id
        projects[project_id] = project_entry

    return routes, projects
