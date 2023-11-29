import os
import requests
import json
from pathlib import Path  # Importa la clase Path desde pathlib

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

# Obtener los datos de tu URL
url_shinyrates = "https://shinyrates.com/data/rate/"
url_pokedex = "https://raw.githubusercontent.com/GaelVM/Datos/main/pokedex2023.json"

response_shinyrates = requests.get(url_shinyrates)
response_pokedex = requests.get(url_pokedex)

# Asegúrate de manejar posibles errores HTTP
response_shinyrates.raise_for_status()
response_pokedex.raise_for_status()

if response_shinyrates.status_code == 200 and response_pokedex.status_code == 200:
    data_shinyrates = response_shinyrates.json()
    data_pokedex = response_pokedex.json()

    formatted_data = []

    for item in data_shinyrates:
        # Buscar el elemento correspondiente en el JSON de la pokedex por nombre
        matching_pokemon = next((pokemon for pokemon in data_pokedex if pokemon["nombre"] == item["name"]), None)

        if matching_pokemon:
            formatted_item = {
                "ID": item["id"],
                "Name": item["name"],
                "Shiny Rate": item["rate"],
                "Sample Size": item["total"],
                "assets": {
                    "image": matching_pokemon["assets"]["image"]
                },
                "primaryType": {
                    "es": matching_pokemon["primaryType"]["es"]
                },
                "secondaryType": {
                    "es": matching_pokemon["secondaryType"]["es"]
                }
            }
            formatted_data.append(formatted_item)

    # Ordenar la lista por "Shiny Rate" en orden ascendente
    sorted_data = sorted(formatted_data, key=lambda x: int(x["Shiny Rate"].replace(",", "").split("/")[1]))

    # Asignar un número secuencial a los elementos
    contador = 1
    for item in sorted_data:
        item["Top Number"] = contador
        contador += 1

    # Define la ruta completa del archivo JSON en la carpeta temporal
    json_file_path = Path(temp_folder) / "shinyrates.json"

    # Guardar el diccionario en un archivo JSON en la carpeta temporal
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(sorted_data, json_file, ensure_ascii=False, indent=2)

    print(f"Datos guardados en {json_file_path}")
