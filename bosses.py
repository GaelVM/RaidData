import requests
from bs4 import BeautifulSoup
import json
import os
import tempfile
import shutil

# Crear una carpeta temporal
temp_dir = tempfile.mkdtemp()

# Definir la ruta del archivo JSON en la carpeta temporal
json_file_path = os.path.join(temp_dir, "raid_data_by_level.json")

# Definir la URL de la página web
url = "https://pokemongo.fandom.com/wiki/List_of_current_Raid_Bosses"

# Realizar la solicitud HTTP y obtener el contenido de la página
response = requests.get(url)

# Verificar si la solicitud fue exitosa
if response.status_code == 200:
    # Parsear el contenido HTML con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar todos los elementos dentro del div principal
    elements = soup.find("div", class_="pogo-list-container bg-raid").find_all("div")

    # Inicializar variables para el título y los datos de la incursión
    raid_level = None
    boss_name = None
    boss_cp = None
    max_capture_cp = None

    # Crear un diccionario para almacenar los datos de incursión agrupados por "Raid Level"
    raid_data_by_level = {}

    for element in elements:
        if element.has_attr("class") and "pogo-list-header" in element["class"]:
            raid_level = element.get_text().strip()
            print("Raid Level:", raid_level)
            raid_data_by_level[raid_level] = []  # Inicializar una lista vacía para el nivel de incursión actual
        elif element.has_attr("class") and "pogo-list-item" in element["class"]:
            raid_info = element.find("div", class_="pogo-list-item-desc")
            no_dex = element.find("div", class_="pogo-list-item-number").text.strip()
            print("No Dex:", no_dex)
            boss_name = raid_info.find("div", class_="pogo-list-item-name").text.strip()
            print("Boss Name:", boss_name)
            boss_cp = raid_info.find("div", class_="pogo-raid-item-desc").find("b", class_="label").next_sibling.strip()
            print("Boss CP:", boss_cp)
            max_capture_cp = raid_info.find("b", text="Max capture CP").find_next("br").next_sibling.strip()
            print("Max Capture CP:", max_capture_cp)
            max_capture_cp_bosst = raid_info.find("div", class_="pogo-raid-item-desc").find("span", class_="pogo-raid-item-wb").text.strip()
            print("Max Capture CP (with Weather Boost):", max_capture_cp_bosst)
            shiny_info = element.find("div", class_="pogo-list-item-image")
            shiny = "Yes" if "shiny" in shiny_info.get("class") else "No"
            print("Shiny:", shiny)
            print("\n")

            # Agregar todos los campos al diccionario raid_data
            raid_data = {
                "No Dex": no_dex,
                "Boss Name": boss_name,
                "Boss CP": boss_cp,
                "Max Capture CP": max_capture_cp,
                "Max Capture CP Bosst": max_capture_cp_bosst,
                "Shiny": shiny
            }
            
            # Agregar el diccionario de datos al nivel de incursión correspondiente
            raid_data_by_level[raid_level].append(raid_data)

            # Guardar el diccionario raid_data_by_level en el archivo JSON en la carpeta temporal
            with open(json_file_path, "w") as json_file:
             json.dump(raid_data_by_level, json_file, indent=4)

# Copiar el archivo JSON al directorio de trabajo del flujo de trabajo
shutil.copy(json_file_path, "./raid_data_by_level.json")