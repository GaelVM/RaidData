import os
import requests
from bs4 import BeautifulSoup
import json

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

url = "https://www.serebii.net/pokemongo/eggs.shtml"
response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table', class_='dextab')  # Buscar la tabla con la clase 'dextab'
    
    data = []

    for row in table.find_all('tr')[1:]:  # Ignorar la primera fila que contiene los encabezados
        columns = row.find_all(['td', 'th'])
        
        # Verificar si hay suficientes columnas antes de acceder a ellas
        if len(columns) >= 6:
            type_imgs = columns[4].find_all("img")
            type_info = {f"Typo{i+1}": img['src'].split('/')[-1].split('.')[0] for i, img in enumerate(type_imgs)}
            
            shiny_img = columns[3].find('img', {'alt': 'Shiny Capable'})
            shiny = "si" if shiny_img else "no"

            entry = {
                "No.": columns[0].text.strip(),
                "Pic": "https://www.serebii.net" + columns[1].find('img')['src'].strip() if columns[1].find('img') else "",
                "Name": columns[3].find('a').text.strip(),
                "Type": type_info,
                "Egg Distance": columns[5].text.strip(),
                "Max CP At Hatch": columns[6].text.strip(),
                "Shiny": shiny
            }
            data.append(entry)
        else:
            print("Advertencia: Fila incompleta, se omite.")


    # Define la ruta completa del archivo JSON en la carpeta temporal
    json_file_path = os.path.join(temp_folder, "eggs.json")

    # Guardar el diccionario en un archivo JSON en la carpeta temporal
    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)

    print(f"Datos guardados en {json_file_path}")

else:
    print(f"Error al obtener la página. Código de estado: {response.status_code}")
