import os
import re
import time
import csv
import json
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def limpiar_nombre(texto):
    texto = texto.lower()
    texto = re.sub(r'[^a-z0-9]+', '_', texto)
    return texto.strip("_")

def descargar_imagen(url, path):
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            with open(path, "wb") as f:
                f.write(r.content)
    except:
        pass


def obtener_obras(driver, museo_link):
    driver.get(museo_link.replace("/partner/", "/explore/collections/") + "?c=assets")
    time.sleep(5)

    seen_links = set()
    data = []

    prev_count = 0
    no_change_count = 0

    while True:
        obras = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/asset/"]')

        for obra in obras:
            try:
                link = obra.get_attribute("href")

                if link in seen_links:
                    continue

                seen_links.add(link)

                titulo = obra.find_element(By.CSS_SELECTOR, "h3").text
                artista = obra.find_element(By.CSS_SELECTOR, "h4").text if obra.find_elements(By.CSS_SELECTOR, "h4") else "Unknown"

                # imagen
                img_url = ""
                try:
                    img = obra.find_element(By.CSS_SELECTOR, "[data-bgsrc]")
                    img_url = img.get_attribute("data-bgsrc")

                    if img_url.startswith("//"):
                        img_url = "https:" + img_url

                    if "=" in img_url:
                        img_url = img_url.split("=")[0] + "=w1000"

                except:
                    pass

                data.append({
                    "titulo": titulo,
                    "artista": artista,
                    "link": link,
                    "img_url": img_url
                })

            except:
                pass

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        if len(seen_links) == prev_count:
            no_change_count += 1
        else:
            no_change_count = 0

        if no_change_count >= 2:
            break

        prev_count = len(seen_links)

    return data


def obtener_detalle(driver, link):
    driver.get(link)
    time.sleep(3)


    descripcion = ""
    try:
        parrafos = driver.find_elements(By.CSS_SELECTOR, "section.WDSAyb p")
        descripcion = " ".join([p.text for p in parrafos])
    except:
        pass

    # metadata
    metadata = {}
    try:
        items = driver.find_elements(By.CSS_SELECTOR, "section.rw8Th li")
        for item in items:
            try:
                key = item.find_element(By.CSS_SELECTOR, "span").text.replace(":", "").strip()
                value = item.text.replace(item.find_element(By.CSS_SELECTOR, "span").text, "").strip()
                metadata[key] = value
            except:
                pass
    except:
        pass

    return descripcion, metadata



driver = webdriver.Chrome()

with open("test.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for museo in reader:
        nombre = limpiar_nombre(museo["nombre"])
        link = museo["link"]

        print(f"\n Procesando museo: {nombre}")

        base_path = f"data/{nombre}"
        images_path = f"{base_path}/images"

        os.makedirs(images_path, exist_ok=True)

        obras = obtener_obras(driver, link)

        dataset = []

        for i, obra in enumerate(obras):
            print(f"{i+1}/{len(obras)}")

            descripcion, metadata = obtener_detalle(driver, obra["link"])


            image_path = ""
            if obra["img_url"]:
                obra_id = obra["link"].split("/")[-1]
                nombre_archivo = f"{limpiar_nombre(obra['titulo'])}_{obra_id}.jpg"
                image_path = f"{images_path}/{nombre_archivo}"

                descargar_imagen(obra["img_url"], image_path)

            dataset.append({
                "titulo": obra["titulo"],
                "artista": obra["artista"],
                "link": obra["link"],
                "descripcion": descripcion,
                "metadata": metadata,
                "imagen": image_path
            })

        with open(f"{base_path}/dataset.json", "w", encoding="utf-8") as f:
            json.dump(dataset, f, ensure_ascii=False, indent=4)


        with open(f"{base_path}/obras.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["titulo", "artista", "link", "imagen"])

            for d in dataset:
                writer.writerow([d["titulo"], d["artista"], d["link"], d["imagen"]])

driver.quit()