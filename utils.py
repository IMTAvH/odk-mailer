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
    # https://odkcentral.upch.edu.pe/-/single/ganT9xIuyBEkCmQ1mRY8cpeIWWzxhi8?st=7hvmW0WI844J9APdTa13h0h14tli31!YsFuEIMY2YBEnlkg0$r1HjJ3sVfbTgSje

    formulario = {
            "form_id": "ganT9xIuyBEkCmQ1mRY8cpeIWWzxhi8",
            "token": "7hvmW0WI844J9APdTa13h0h14tli31!YsFuEIMY2YBEnlkg0$r1HjJ3sVfbTgSje"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&d[/data/consent/part_id]={valor_id}"


def construir_url_part1(valor_id, edad):
    return_url = f"https://odkcentral.upch.edu.pe/next?part_id={quote(valor_id)}&form=f2"
    # valor_codificado = quote_plus(valor_id)  # para escapar caracteres especiales
    formulario = {
        "form_id": "oJaqbizarAl2a5ITzH2YsX2gjzETtZc",
        "token": "C$6e3qVTuUep24hjvlfHMPRTudVzhwhmKibeXTSAapZgwBJeGSksmVN7Htle9iYj",
        "part_id": "d[/data/sexual_reproductive_health/part_id_2]",
        "age": "d[/data/general_data/Q1.3_age]"
        }
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}&{formulario['age']}={edad}&returnUrl={quote(return_url, safe='')}"

def url_part1_encadenado(part_id, edad):
    part_id = str(part_id)
    edad = str(edad)

    formularios = [

        # {
        #     "form_id": "P8IjtH0MW7hlpoWvkumJiatn8FlqWfX",
        #     "token": "tXEQPaV2Km7nds8sokNf3qA3EEF$81Op!JilgF!SrnMg2QBggAcBZG8Cc5amztQx",
        #     "part_id": "d[/data/End/part_id_10]"
        # },
        # Form Part 9
        # https://odkcentral.upch.edu.pe/-/single/P8IjtH0MW7hlpoWvkumJiatn8FlqWfX?st=tXEQPaV2Km7nds8sokNf3qA3EEF$81Op!JilgF!SrnMg2QBggAcBZG8Cc5amztQx
        # {
        #     "form_id": "7kUSBjynPl8sKAN3ofMn7yaIcn4A1eu",
        #     "token": "nroBNIP!toKptniGoRNmrOkd3DBPEdoP8nhOE6YeD9PiRZ0CnYJ5A9nZ4PpDldq3",
        #     "part_id": "d[/data/mental_health_emotional_wellbeing/part_id_9]"
        # },
        # Form Part 8
        # https://odkcentral.upch.edu.pe/-/single/7kUSBjynPl8sKAN3ofMn7yaIcn4A1eu?st=nroBNIP!toKptniGoRNmrOkd3DBPEdoP8nhOE6YeD9PiRZ0CnYJ5A9nZ4PpDldq3
        # {
        #     "form_id": "AYQjTpJK4kdav1PS7wYgqhxylBfyhkQ",
        #     "token": "DQIdbtlrmSb!XGKnBXkPArgCGcYIy8rJIswCOOhCJd1kSTwKEJpxaomEmYsbpUav",
        #     "part_id": "d[/data/menstrual_health_spm/part_id_8]"
        # },
        # Form Part 7
        # https://odkcentral.upch.edu.pe/-/single/AYQjTpJK4kdav1PS7wYgqhxylBfyhkQ?st=DQIdbtlrmSb!XGKnBXkPArgCGcYIy8rJIswCOOhCJd1kSTwKEJpxaomEmYsbpUav
        # {
        #     "form_id": "O7Bx9vT4OThP2DpN2yiR7SrPiinLMFs",
        #     "token": "GVadPgjmef7A2uY728VpF8Meda8NPawfb5hnhHuGv8H!Y5UIQ$qgw32AlpGYiLpw",
        #     "part_id": "d[/data/srh_menoapause_yes_or_likeky/part_id_7]"
        # },
        # Form Part 6
        # https://odkcentral.upch.edu.pe/-/single/O7Bx9vT4OThP2DpN2yiR7SrPiinLMFs?st=GVadPgjmef7A2uY728VpF8Meda8NPawfb5hnhHuGv8H!Y5UIQ$qgw32AlpGYiLpw
        # {
        #     "form_id": "ONirzMPf24fbLc2xLHuUHD1SHxwIw7d",
        #     "token": "WtkFihLyehW96FDJoW0r0WjljkNgRvABx5Lgm6QNm!9RnZqZKvt9469Tll3hzIHl",
        #     "part_id": "d[/data/sexual_reproductive_health/part_id_6]"
        # },
        # Form Part 5
        # https://odkcentral.upch.edu.pe/-/single/ONirzMPf24fbLc2xLHuUHD1SHxwIw7d?st=WtkFihLyehW96FDJoW0r0WjljkNgRvABx5Lgm6QNm!9RnZqZKvt9469Tll3hzIHl
        # {
        #     "form_id": "v3NUCyLIXypt4ocz0YbKg5uoxRY5BYD",
        #     "token": "qXltW8xMvAIRils99XG9IUYvoNtRz53xPcB9V2fEiz6kbQtFOV8swVwZze3x$4EL",
        #     "part_id": "d[/data/general_health/part_id_5]"
        # },
        # Form Part 4
        # https://odkcentral.upch.edu.pe/-/single/v3NUCyLIXypt4ocz0YbKg5uoxRY5BYD?st=qXltW8xMvAIRils99XG9IUYvoNtRz53xPcB9V2fEiz6kbQtFOV8swVwZze3x$4EL
        # {
        #     "form_id": "vmngcom1ZaTITHFj5MHfJefN6Oevjk0",
        #     "token": "xU2nudC!h$gAzcDoe5TcqK5pz4RQfAUN0HqtyHRrEW1oy4mcvfz$rRBsNnQzW0Mn",
        #     "part_id": "d[/data/personal_hygiene/part_id_4]"
        # },
        # Form Part 3
        # https://odkcentral.upch.edu.pe/-/single/vmngcom1ZaTITHFj5MHfJefN6Oevjk0?st=xU2nudC!h$gAzcDoe5TcqK5pz4RQfAUN0HqtyHRrEW1oy4mcvfz$rRBsNnQzW0Mn
        {
            "form_id": "fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX",
            "token": "d4YCxBKvsx$tkKOWB6OD0RPijaxIAc1ktxG58KvPKFaQYTRKWNsQUYjTO$aCJW9f",
            "part_id": "d[/data/End/part_id_3]"
        },
        # Form Part 2
        # https://odkcentral.upch.edu.pe/-/single/fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX?st=d4YCxBKvsx$tkKOWB6OD0RPijaxIAc1ktxG58KvPKFaQYTRKWNsQUYjTO$aCJW9f
        {
            "form_id": "oJaqbizarAl2a5ITzH2YsX2gjzETtZc",
            "token": "C$6e3qVTuUep24hjvlfHMPRTudVzhwhmKibeXTSAapZgwBJeGSksmVN7Htle9iYj",
            "part_id": "d[/data/sexual_reproductive_health/part_id_2]",
            "age": "d[/data/general_data/Q1.3_age]"
        },
        # Form Part 1
        # https://odkcentral.upch.edu.pe/-/single/oJaqbizarAl2a5ITzH2YsX2gjzETtZc?st=C$6e3qVTuUep24hjvlfHMPRTudVzhwhmKibeXTSAapZgwBJeGSksmVN7Htle9iYj
    ]

    base = "https://odkcentral.upch.edu.pe/-/single"
    url_final = None

    for entry in formularios:
        url = f"{base}/{entry['form_id']}?st={entry['token']}"
        url += f"&{quote(entry['part_id'])}={quote(part_id)}"
        if "age" in entry:
            url += f"&{quote(entry['age'])}={quote(edad)}"
        if url_final:
            url += f"&returnUrl={quote(url_final, safe='')}"
        url_final = url

    return url_final  # Última URL construida, la visible al usuario


def construir_url_part2(valor_id):
    # valor_codificado = quote_plus(valor_id)  # para escapar caracteres especiales
    formulario = {
            "form_id": "fgLy1rY5M1YOeycvuIxqMHsUNBYoZCX",
            "token": "d4YCxBKvsx$tkKOWB6OD0RPijaxIAc1ktxG58KvPKFaQYTRKWNsQUYjTO$aCJW9f",
            "part_id": "d[/data/End/part_id_3]"
        },
    return f"https://odkcentral.upch.edu.pe/-/single/{formulario['form_id']}?st={formulario['token']}&{formulario['part_id']}={valor_id}"

# url = url_part1_encadenado("732f7e95d4eaf9bfff443a401865dd7783b88bc1704ff78f265cc42a19997ba8", 70)
# print(url)


# Form pre-registro
# https://odkcentral.upch.edu.pe/-/single/XbQEbCiDjg5nAytcJfE4iUNU0vtFRpv?st=5WUuC$XP5g!CNJEyhjBqKkLEPtcILEX3cJZg2HwVvCoGV6mKg3fLSJ9oo$UKZ$CG





















# Laura 2.0 - Encuesta - Nacional - Part 2 (entrenamiento TC Lima)