import os
import requests
from bs4 import BeautifulSoup
import json

# Define la carpeta temporal
temp_folder = "temp"

# Verifica si la carpeta temporal ya existe, y si no, créala
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)

url = "https://pokemongolive.com/news/?hl=es"

# Obtener el contenido HTML de la página
response = requests.get(url)
html = response.text

# Analizar el HTML con BeautifulSoup
soup = BeautifulSoup(html, "html.parser")

# Encontrar el div con la clase "blogList__posts"
blog_posts_div = soup.find("div", class_="blogList__posts")

# Encontrar todas las etiquetas "a" dentro del div
post_links = blog_posts_div.find_all("a", class_="blogList__post")

# Lista para almacenar los datos de cada entrada
posts_data = []

# Iterar sobre las etiquetas encontradas y extraer la información
for post_link in post_links:
    post_url = "https://pokemongolive.com" + post_link["href"]
    post_image = post_link.find("img")["src"]
    post_date = post_link.find("div", class_="blogList__post__content__date").text.strip()
    post_title = post_link.find("div", class_="blogList__post__content__title").text.strip()

    # Agregar los datos a la lista
    posts_data.append({
        "URL": post_url,
        "Image": post_image,
        "Date": post_date,
        "Title": post_title
    })

# Define la ruta completa del archivo JSON en la carpeta temporal
json_file_path = os.path.join(temp_folder, "noticias.json")

# Guardar el diccionario en un archivo JSON en la carpeta temporal
with open(json_file_path, "w", encoding="utf-8") as json_file:
    json.dump(posts_data, json_file, ensure_ascii=False, indent=2)

print(f"Datos guardados en {json_file_path}")
