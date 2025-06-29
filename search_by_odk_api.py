from dotenv import load_dotenv

load_dotenv()

import os
import requests
import xmltodict

def get_odk_token():
    base_url = os.getenv("ODK_BASE_URL")
    username = os.getenv("ODK_USERNAME")
    password = os.getenv("ODK_PASSWORD")

    url = f"{base_url}/v1/sessions"
    payload = {"email": username, "password": password}
    response = requests.post(url, json=payload)

    if response.status_code == 200:
        token = response.json().get("token")
        print("✅ Token generado.")
        return token
    else:
        print(f"❌ Error al obtener token: {response.status_code} - {response.text}")
        return None

def buscar_correo_en_submissions(participant_id):
    base_url = os.getenv("ODK_BASE_URL")
    token = get_odk_token()
    project_id = os.getenv("ODK_PROJECT_ID", 2)
    form_id = os.getenv("ODK_FORM_PREREGISTRO")

    if not all([base_url, token, form_id]):
        print("❌ Faltan datos en el entorno")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    base_url = base_url.rstrip("/")
    list_url = f"{base_url}/v1/projects/{project_id}/forms/{form_id}/submissions"

    response = requests.get(list_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al obtener submissions: {response.status_code}")
        return None

    submissions = response.json()

    for sub in submissions:
        instance_id = sub["instanceId"]
        xml_url = f"{list_url}/{instance_id}.xml"
        xml_resp = requests.get(xml_url, headers=headers)

        if xml_resp.status_code != 200:
            continue

        try:
            parsed = xmltodict.parse(xml_resp.text)
            data = parsed["data"]["participantes"]
            if data.get("participante_id") == participant_id:
                print("✅ Participante encontrada")
                print(f"✅ Correo: {data['correo']}")
                return data["correo"]
        except Exception:
            continue

    print(f"⚠️ No se encontró el participant_id: {participant_id} en ningún submission")
    return None

def buscar_edad_en_submissions(participant_id):
    base_url = os.getenv("ODK_BASE_URL")
    token = get_odk_token()
    project_id = os.getenv("ODK_PROJECT_ID", 2)
    form_id = os.getenv("ODK_FORM_PREREGISTRO")

    if not all([base_url, token, form_id]):
        print("❌ Faltan datos en el entorno")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    base_url = base_url.rstrip("/")
    list_url = f"{base_url}/v1/projects/{project_id}/forms/{form_id}/submissions"

    response = requests.get(list_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al obtener submissions: {response.status_code}")
        return None

    submissions = response.json()

    for sub in submissions:
        instance_id = sub["instanceId"]
        xml_url = f"{list_url}/{instance_id}.xml"
        xml_resp = requests.get(xml_url, headers=headers)

        if xml_resp.status_code != 200:
            continue

        try:
            parsed = xmltodict.parse(xml_resp.text)
            data = parsed["data"]["participantes"]
            if data.get("participante_id") == participant_id:
                print(f"✅ Participante encontrada")
                print(f"✅ Edad: {data['edad']}")
                return data["edad"]
        except Exception:
            continue

    print(f"⚠️ No se encontró el participant_id: {participant_id} en ningún submission")
    return None

def buscar_submissions_en_p1(participant_id):
    base_url = os.getenv("ODK_BASE_URL")
    token = get_odk_token()
    project_id = os.getenv("ODK_PROJECT_ID", 2)
    form_id = os.getenv("ODK_FORM_EN_P1")

    if not all([base_url, token, form_id]):
        print("❌ Faltan datos en el entorno")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    base_url = base_url.rstrip("/")
    list_url = f"{base_url}/v1/projects/{project_id}/forms/{form_id}/submissions"

    response = requests.get(list_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al obtener submissions: {response.status_code}")
        return None

    submissions = response.json()

    for sub in submissions:
        instance_id = sub["instanceId"]
        xml_url = f"{list_url}/{instance_id}.xml"
        xml_resp = requests.get(xml_url, headers=headers)

        if xml_resp.status_code != 200:
            continue

        try:
            parsed = xmltodict.parse(xml_resp.text)
            data = parsed["data"]["preamble"]
            if data.get("part_id_2") == participant_id:
                print(f"✅ Participante encontrada")
                print(f"✅ EN P1: {data['complete_p1']}")
                return data["complete_p1"]
        except Exception:
            continue

    print(f"⚠️ No se encontró el participant_id: {participant_id} en ningún submission")
    return None

def buscar_submissions_en_p2(participant_id):
    base_url = os.getenv("ODK_BASE_URL")
    token = get_odk_token()
    project_id = os.getenv("ODK_PROJECT_ID", 2)
    form_id = os.getenv("ODK_FORM_EN_P2")

    if not all([base_url, token, form_id]):
        print("❌ Faltan datos en el entorno")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    base_url = base_url.rstrip("/")
    list_url = f"{base_url}/v1/projects/{project_id}/forms/{form_id}/submissions"

    response = requests.get(list_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al obtener submissions: {response.status_code}")
        return None

    submissions = response.json()

    for sub in submissions:
        instance_id = sub["instanceId"]
        xml_url = f"{list_url}/{instance_id}.xml"
        xml_resp = requests.get(xml_url, headers=headers)

        if xml_resp.status_code != 200:
            continue

        try:
            parsed = xmltodict.parse(xml_resp.text)
            data = parsed["data"]["preamble"]
            if data.get("part_id_3") == participant_id:
                print(f"✅ Participante encontrada")
                print(f"✅ EN P1: {data['complete_p2']}")
                return data["complete_p2"]
        except Exception:
            continue

    print(f"⚠️ No se encontró el participant_id: {participant_id} en ningún submission")
    return None

def buscar_submissions_en_p3(participant_id):
    base_url = os.getenv("ODK_BASE_URL")
    token = get_odk_token()
    project_id = os.getenv("ODK_PROJECT_ID", 2)
    form_id = os.getenv("ODK_FORM_EN_P3")

    if not all([base_url, token, form_id]):
        print("❌ Faltan datos en el entorno")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    base_url = base_url.rstrip("/")
    list_url = f"{base_url}/v1/projects/{project_id}/forms/{form_id}/submissions"

    response = requests.get(list_url, headers=headers)
    if response.status_code != 200:
        print(f"❌ Error al obtener submissions: {response.status_code}")
        return None

    submissions = response.json()

    for sub in submissions:
        instance_id = sub["instanceId"]
        xml_url = f"{list_url}/{instance_id}.xml"
        xml_resp = requests.get(xml_url, headers=headers)

        if xml_resp.status_code != 200:
            continue

        try:
            parsed = xmltodict.parse(xml_resp.text)
            data = parsed["data"]["preamble"]
            if data.get("part_id_4") == participant_id:
                print(f"✅ Participante encontrada")
                print(f"✅ EN P3: {data['complete_p3']}")
                return data["complete_p3"]
        except Exception:
            continue

    print(f"⚠️ No se encontró el participant_id: {participant_id} en ningún submission")
    return None

def buscar_datos_en_entidad_participantes(phone):
    base_url = os.getenv("ODK_BASE_URL")
    token = get_odk_token()
    project_id = os.getenv("ODK_PROJECT_ID", 1)
    entity_table = "participantes"

    if not all([base_url, token, project_id, entity_table]):
        print("❌ Faltan datos en el entorno")
        return None

    headers = {"Authorization": f"Bearer {token}"}
    base_url = base_url.rstrip("/")
    list_url = f"{base_url}/v1/projects/{project_id}/datasets/{entity_table}/entities"

    response = requests.get(list_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Error al obtener entidades: {response.status_code}")
        return None

    entities = response.json()

    numero_tel = phone
    for entity in entities:
        label = entity.get("currentVersion", {}).get("label")
        if not label:
            continue
        if label == numero_tel:
            uuid = entity.get("uuid")
            print(f"✅ Posible entidad encontrada con label: {label} (UUID: {uuid})")
            entity_url = f"{list_url}/{uuid}"
            detail_resp = requests.get(entity_url, headers=headers)

            if detail_resp.status_code != 200:
                print(f"⚠️ No se pudo obtener el detalle de entidad {uuid}")
                continue

            detail = detail_resp.json()
            data = detail.get("currentVersion", {}).get("data", {})
            print(data)
            return data

    print(f"⚠️ No se encontró el telefono: {numero_tel} en entidades")
    return None
