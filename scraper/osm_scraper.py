import pandas as pd
import osmnx as ox
from pathlib import Path

OUTPUT_PATH = Path("data/raw")
OUTPUT_PATH.mkdir(parents=True, exist_ok=True)

print("Buscando estabelecimentos no OpenStreetMap...")

tags = {
    "brand": "McDonald's"
}

gdf = ox.features_from_place(
    "São Paulo, Brazil",
    tags=tags
)

columns_of_interest = [
    "name",
    "brand",
    "addr:street",
    "addr:housenumber",
    "addr:city",
    "addr:postcode",
    "phone",
    "website",
    "geometry"
]

available_columns = [
    col for col in columns_of_interest
    if col in gdf.columns
]

df = gdf[available_columns].copy()

df["lat"] = gdf.geometry.centroid.y
df["lon"] = gdf.geometry.centroid.x

df.reset_index(inplace=True)

df.to_csv(
    OUTPUT_PATH / "osm_mcdonalds.csv",
    index=False
)

print(f"{len(df)} registros salvos.")