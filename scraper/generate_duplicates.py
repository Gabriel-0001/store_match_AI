import random
import pandas as pd
from pathlib import Path

INPUT_FILE = "data/raw/osm_mcdonalds.csv"
OUTPUT_FILE = "data/raw/osm_mcdonalds_dirty.csv"

random.seed(42)

df = pd.read_csv(INPUT_FILE)

dirty_rows = []

for _, row in df.iterrows():

    new_row = row.copy()

    if pd.notna(row.get("name")):

        name = str(row["name"])

        transformations = [
            lambda x: x.upper(),
            lambda x: x.replace("McDonald's", "Mc Donalds"),
            lambda x: x.replace("McDonald's", "MCDONALDS"),
            lambda x: x.replace("Restaurant", "Rest."),
        ]

        transformation = random.choice(transformations)

        try:
            new_row["name"] = transformation(name)
        except Exception:
            pass

    if pd.notna(row.get("lat")):
        new_row["lat"] = float(row["lat"]) + random.uniform(-0.0005, 0.0005)

    if pd.notna(row.get("lon")):
        new_row["lon"] = float(row["lon"]) + random.uniform(-0.0005, 0.0005)

    new_row["is_duplicate"] = 1

    dirty_rows.append(new_row)

dirty_df = pd.DataFrame(dirty_rows)

dirty_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print(f"{len(dirty_df)} registros gerados.")