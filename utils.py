import requests
import os

processed_ids = set()

def is_duplicate(instance_id: str) -> bool:
    if instance_id in processed_ids:
        return True
    processed_ids.add(instance_id)
    return False

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

def construir_url(valor_id):
    # valor_codificado = quote_plus(valor_id)  # para escapar caracteres especiales
    return f"https://odkcentral.upch.edu.pe/-/single/oJaqbizarAl2a5ITzH2YsX2gjzETtZc?st=iBuuWmJsoZ!tVBhBiszLnN7BZbtI7zlepFvpgFGJWqBzSPC6riGbcIpduEAN$L39&d[/data/part_id]={valor_id}"

