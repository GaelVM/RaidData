import os
import requests
from bs4 import BeautifulSoup
import json

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

url = "https://www.serebii.net/pokemongo/raidbattles.shtml"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    # Busca todas las etiquetas <h3> con texto que contiene "List"
    list_headings = soup.find_all("h3", string=lambda text: "List" in text)

    all_data = {}

    for heading in list_headings:
        # Encuentra la tabla con la clase "dextab" y alineada al centro
        raid_boss_table = heading.find_next("table", class_="dextab", align="center")

        if raid_boss_table:
            # Lista para almacenar los datos de las filas
            raid_boss_data = []

            # Itera sobre las filas de la tabla, omitiendo la primera (cabecera)
            for row in raid_boss_table.find_all("tr")[1:]:
                # Extrae los datos de cada celda
                columns = row.find_all(["td", "th"])
                
                # Asegúrate de que hay suficientes elementos en la lista antes de acceder a ellos
                if len(columns) >= 6:
                    # Extrae la URL de la imagen desde la etiqueta <img> y agrega la parte base
                    img_url = "https://www.serebii.net" + (columns[1].find("img")['src'] if columns[1].find("img") else "")

                    # Extrae los nombres de los archivos de tipo
                    type_imgs = columns[4].find_all("img")
                    type_info = {f"Typo{i+1}": img['src'].split('/')[-1].split('.')[0] for i, img in enumerate(type_imgs)}

                    # Extrae la información de CP y formatea como un diccionario
                    cp_text = columns[6].get_text(strip=True)
                    cp_info = {
                        "Normal": cp_text.split(":")[1].split("Boosted")[0].strip(),
                        "Boosted": cp_text.split(":")[2].strip()
                    }

                    # Verifica la presencia de la imagen "shiny.png"
                    shiny_img = columns[3].find("img", src="/pokemongo/icons/shiny.png")
                    shiny_status = "yes" if shiny_img else "no"

                    data = {
                        "No.": columns[0].get_text(strip=True),
                        "Pic": img_url,
                        "Name": columns[3].get_text(strip=True),  # Mantenido el orden original
                        "Type": type_info,
                        "CP": columns[5].get_text(strip=True),
                        "Max. CP At Capture": cp_info,
                        "Shiny": shiny_status
                    }

                    # Agrega los datos de la fila a la lista
                    raid_boss_data.append(data)

            # Agrega los datos al diccionario principal con el título como clave
            all_data[heading.get_text(strip=True)] = raid_boss_data

    # Define la ruta completa del archivo JSON en la carpeta temporal
    json_file_path = os.path.join(temp_folder, "bossraid.json")

    # Guardar el diccionario en un archivo JSON en la carpeta temporal
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(all_data, json_file, ensure_ascii=False, indent=2)

    print(f"Datos guardados en {json_file_path}")

else:
    print(f"Error al obtener la página. Código de estado: {response.status_code}")
