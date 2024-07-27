import json
import requests
import os

# Obtener el JSON original desde la URL
url = "https://raw.githubusercontent.com/GaelVM/DataDuck/data/events.json"
response = requests.get(url)
original_json = response.json()

# Filtrar eventos con eventType "raid-hour"
filtered_raid_events = [event for event in original_json if event.get("eventType") == "raid-hour"]

# Crear un nuevo JSON con los datos filtrados
new_json = []

# Procesar eventos de "raid-hour"
for event in filtered_raid_events:
    # Eliminar "Raid Hour" del nombre y mantener solo el nombre del Pokémon
    pokemon_name = event["name"].replace(" Raid Hour", "")
    
    # Manejar el caso donde se encuentra "Forme"
    if "Forme" in pokemon_name:
        parts = pokemon_name.split(" Forme ")
        formatted_name = f"{parts[1]} {parts[0]}"
        fm_value = parts[0] if len(parts) > 1 else ""
    else:
        formatted_name = pokemon_name
        fm_value = None

    new_event = {
        "name": formatted_name.strip(),
        "start": event["start"],  # Extraer start del JSON original
        "end": event["end"],      # Extraer end del JSON original
        "extraData": event["extraData"]
    }
    
    # Añadir la clave "fm" si corresponde
    if fm_value:
        new_event["fm"] = fm_value.strip()

    new_json.append(new_event)

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# Define la ruta completa del archivo JSON en la carpeta temporal
json_file_path = os.path.join(temp_folder, "raid_hour.json")

# Escribir el nuevo JSON en un archivo
with open(json_file_path, "w") as file:
    json.dump(new_json, file, indent=4, ensure_ascii=False)

print("Nuevo JSON creado con éxito.")
