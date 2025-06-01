import requests
import os
from urllib.parse import quote

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

def construir_url_consent(valor_id):
    # valor_codificado = quote_plus(valor_id)  # para escapar caracteres especiales

    # Form consentimiento informado
    # https://odkcentral.upch.edu.pe/-/single/ganT9xIuyBEkCmQ1mRY8cpeIWWzxhi8?st=YlRK8XkXCJsl3aX0uCcbawjukW8hZZewEd8hppK1H76bWMnzwuIyC9OcIgIwzdYs

    formulario = {
            "form_id": "ganT9xIuyBEkCmQ1mRY8cpeIWWzxhi8",
            "token": "YlRK8XkXCJsl3aX0uCcbawjukW8hZZewEd8hppK1H76bWMnzwuIyC9OcIgIwzdYs"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&d[/data/preamble/part_id]={valor_id}"

def construir_url_part1(valor_id, edad):
    # https://odkcentral.upch.edu.pe/-/single/oJaqbizarAl2a5ITzH2YsX2gjzETtZc?st=Ai6eTLM1bVT0MnYHivkTxXejfKiJLISTiexXD6hZF9rLr39ilDt6PS$n0zV4VbAG
    formulario = {
        "form_id": "oJaqbizarAl2a5ITzH2YsX2gjzETtZc",
        "token": "Ai6eTLM1bVT0MnYHivkTxXejfKiJLISTiexXD6hZF9rLr39ilDt6PS$n0zV4VbAG",
        "part_id": "d[/data/preamble/part_id_2]",
        "age": "d[/data/general_data/Q1.3_age]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}&{formulario['age']}={edad}"

def construir_url_part2(valor_id):
    # https://odkcentral.upch.edu.pe/-/single/fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX?st=l65vr7s7G80yoQAWHGnWXHOIWT!JeudSgB6CfxhOMIow4LK7rirRypW!mExW!0g2
    formulario = {
        "form_id": "fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX",
        "token": "l65vr7s7G80yoQAWHGnWXHOIWT!JeudSgB6CfxhOMIow4LK7rirRypW!mExW!0g2",
        "part_id": "d[/data/preamble/part_id_3]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"

def construir_url_part3(valor_id):
    # https://odkcentral.upch.edu.pe/-/single/vmngcom1ZaTITHFj5MHfJefN6Oevjk0?st=pNFemRmzNQmwZ8hYzdSo3ttz$jFNlIm9PKCcygRm9duzJOC6CJ3vIGvt1NI5dYm4
    formulario = {
        "form_id": "vmngcom1ZaTITHFj5MHfJefN6Oevjk0",
        "token": "pNFemRmzNQmwZ8hYzdSo3ttz$jFNlIm9PKCcygRm9duzJOC6CJ3vIGvt1NI5dYm4",
        "part_id": "d[/data/preamble/part_id_4]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"
