import os
import requests
from bs4 import BeautifulSoup
import json

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

url = "https://www.serebii.net/pokemongo/shiny.shtml"
response = requests.get(url)

# Diccionario de traducción
translation_dict = {
    "Available when encountered": "Disponible cuando se encuentra",
    "Only available when spawning in events": "Solo disponible durante eventos",
    "Evolve Shiny": "Evolucionar"
}

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='dextab')  # Buscar la tabla con la clase 'dextab'
    
    data = []

    for row in table.find_all('tr')[1:]:  # Ignorar la primera fila que contiene los encabezados
        columns = row.find_all('td')
        
        # Verificar si hay suficientes columnas antes de acceder a ellas
        if len(columns) >= 5:

            # Obtener el valor de Method y traducir si es necesario
            method_value = columns[5].text.strip()
            translated_method = method_value

            for key in translation_dict:
                if key in method_value:
                    translated_method = method_value.replace(key, translation_dict[key])
                    break

            entry = {
                "No.": columns[0].text.strip(),
                "Pic": "https://www.serebii.net" + columns[1].find('img')['src'].strip() if columns[1].find('img') else "",
                "Name": columns[3].find('a').text.strip(),
            
                "Method": translated_method
            }
            data.append(entry)
        else:
            print(f"Advertencia: Fila incompleta con {len(columns)} columnas, se omite.")

    # Define la ruta completa del archivo JSON en la carpeta temporal
    json_file_path = os.path.join(temp_folder, "shinys.json")

    # Guardar el diccionario en un archivo JSON en la carpeta temporal
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

    print(f"Datos guardados en {json_file_path}")

else:
    print(f"Error al obtener la página. Código de estado: {response.status_code}")
