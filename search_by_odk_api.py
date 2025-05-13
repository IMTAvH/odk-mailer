import requests
import os
from utils import get_odk_token  # o donde la tengas definida
from dotenv import load_dotenv
load_dotenv()

import os
import requests
import xmltodict
from utils import get_odk_token

def buscar_correo_en_submissions(participant_id):
    base_url = os.getenv("ODK_BASE_URL")
    token = get_odk_token()
    project_id = os.getenv("ODK_PROJECT_ID", 1)
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
                print(f"✅ Correo encontrado: {data['correo']}")
                return data["correo"]
        except Exception:
            continue

    print(f"⚠️ No se encontró el participant_id: {participant_id} en ningún submission")
    return None

