import requests
import os
import json
import csv
from time import sleep
import re
import unicodedata


BASE_URL = "https://collectionapi.metmuseum.org/public/collection/v1"

# carpeta base
BASE_DIR = os.path.join("data", "the_metropolitan_museum_of_art")
IMG_DIR = os.path.join(BASE_DIR, "images")

os.makedirs(IMG_DIR, exist_ok=True)


def limpiar_nombre(nombre):
    # quitar acentos
    nombre = unicodedata.normalize('NFKD', nombre)
    nombre = nombre.encode('ascii', 'ignore').decode('ascii')


    nombre = nombre.lower()


    nombre = nombre.replace(" ", "_")

    nombre = re.sub(r'[^a-z0-9_]', '', nombre)

    return nombre



search_url = f"{BASE_URL}/search"
params = {
    "q": "painting",
    "hasImages": "true"
}

print("Buscando obras...")
search_res = requests.get(search_url, params=params).json()
object_ids = search_res.get("objectIDs", [])

print(f"Total encontrados: {len(object_ids)}")


data = []

for i, obj_id in enumerate(object_ids):
    print(f"[{i+1}/{len(object_ids)}] Procesando ID {obj_id}")

    try:
        obj_url = f"{BASE_URL}/objects/{obj_id}"
        obj = requests.get(obj_url).json()

        if not obj.get("isPublicDomain") or not obj.get("primaryImage"):
            continue

        record = {
            "objectID": obj.get("objectID"),
            "title": obj.get("title"),
            "artist": obj.get("artistDisplayName"),
            "artistNationality": obj.get("artistNationality"),
            "objectDate": obj.get("objectDate"),
            "medium": obj.get("medium"),
            "dimensions": obj.get("dimensions"),
            "department": obj.get("department"),
            "culture": obj.get("culture"),
            "country": obj.get("country"),
            "classification": obj.get("classification"),
            "image": obj.get("primaryImage"),
            "objectURL": obj.get("objectURL")
        }

        data.append(record)


        img_url = obj["primaryImage"]

        titulo = obj.get("title", "sin_titulo")
        nombre_limpio = limpiar_nombre(titulo)
        img_path = os.path.join(IMG_DIR, f"{nombre_limpio}_{obj_id}.jpg")

        img_data = requests.get(img_url).content
        with open(img_path, "wb") as f:
            f.write(img_data)

        sleep(0.2)

    except Exception as e:
        print(f"Error con {obj_id}: {e}")


json_path = os.path.join(BASE_DIR, "dataset.json")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("JSON guardado.")

csv_path = os.path.join(BASE_DIR, "obras.csv")

if data:
    keys = data[0].keys()

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

print("CSV guardado.")
print(f"Total obras descargadas: {len(data)}")