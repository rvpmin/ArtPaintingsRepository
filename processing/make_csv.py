import os
import json
import csv

DATA_DIR = "data"


for museo in os.listdir(DATA_DIR):
    museo_path = os.path.join(DATA_DIR, museo)

    if not os.path.isdir(museo_path):
        continue

    json_path = os.path.join(museo_path, "dataset.json")

    if not os.path.exists(json_path):
        print(f"{museo} no tiene dataset.json")
        continue

    print(f"\nProcesando {museo}...")


    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)


    metadata_keys = set()

    for item in data:
        metadata = item.get("metadata", {})
        metadata_keys.update(metadata.keys())

    metadata_keys = sorted(metadata_keys)


    base_fields = ["titulo", "artista", "link", "descripcion", "imagen"]
    fieldnames = base_fields + metadata_keys


    csv_path = os.path.join(museo_path, "dataset.csv")

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for item in data:
            row = {}


            for field in base_fields:
                row[field] = item.get(field, "")


            metadata = item.get("metadata", {})
            for key in metadata_keys:
                row[key] = metadata.get(key, "")

            writer.writerow(row)

    print(f"CSV guardado en {csv_path}")