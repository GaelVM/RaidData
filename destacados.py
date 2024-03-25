import json
import requests
import os

# Traducciones de los bonus
bonus_translations = {
    "2× Catch Candy": "Doble de caramelos por captura",
    "2× Catch XP": "Doble de experiencia por captura",
    "2× Catch Stardust": "Doble de polvo estelar por captura",
    "2× Transfer Candy": "Doble de caramelos por transferencia",
    "2× Evolution XP": "Doble de experiencia por evolución",
    "2× Transfer Candy and Increased Transfer Candy XL Chance": "Doble de caramelos por transferencia y mayor probabilidad de obtener caramelos XL"
}

# Obtener el JSON original desde la URL
url = "https://raw.githubusercontent.com/GaelVM/DataDuck/data/events.json"
response = requests.get(url)
original_json = response.json()

# Filtrar eventos con eventType "pokemon-spotlight-hour"
filtered_events = [event for event in original_json if event.get("eventType") == "pokemon-spotlight-hour"]

# Crear un nuevo JSON con los datos filtrados y traducidos
new_json = []
for event in filtered_events:
    bonus = event["extraData"]["spotlight"].get("bonus")
    if bonus:
        translated_bonus = bonus_translations.get(bonus)
        event["extraData"]["spotlight"]["bonusimg"] = bonus
        event["extraData"]["spotlight"]["bonus"] = translated_bonus if translated_bonus else bonus
    new_event = {
        "name": f"Hora destacada de: {event['extraData']['spotlight']['name']}",
        "extraData": event["extraData"]["spotlight"]
    }
    new_json.append(new_event)

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# Define la ruta completa del archivo JSON en la carpeta temporal
json_file_path = os.path.join(temp_folder, "destacados.json")

# Escribir el nuevo JSON en un archivo
with open(json_file_path, "w") as file:
    json.dump(new_json, file, indent=4, ensure_ascii=False)

print("Nuevo JSON creado con éxito.")
