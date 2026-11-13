# B1 - Python intermedio para datos
# Autor: Oscar Moreno Hoyos

from pathlib import Path
import argparse
import requests
import pandas as pd
import geopandas as gpd

parser = argparse.ArgumentParser()
parser.add_argument(
    "--datos",
    default="datos/veredas_boyaca.geojson"
)
args = parser.parse_args()

# PARTE 1 - Consultar veredas de Tunja
url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

params = {
    "where": "NOMB_MPIO = 'TUNJA'",
    "outFields": "NOMB_MPIO,NOMBRE_VER,CODIGO_VER",
    "outSR": "4326",
    "f": "geojson"
}

r = requests.get(url, params=params, timeout=120)
r.raise_for_status()
respuesta = r.json()

if "error" in respuesta:
    raise RuntimeError(respuesta["error"])

tunja = gpd.GeoDataFrame.from_features(
    respuesta["features"], crs=4326
)

print("=" * 65)
print("B1 - PYTHON INTERMEDIO PARA DATOS")
print("=" * 65)

print("\nPARTE 1 - VEREDAS DE TUNJA")
print("Estado HTTP:", r.status_code)
print("Cantidad de veredas:", len(tunja))
print(tunja["NOMBRE_VER"].to_string(index=False))

# PARTE 2 - Municipios con mas veredas
archivo = Path(args.datos)
gdf = gpd.read_file(archivo)

tabla = pd.DataFrame(gdf.drop(columns="geometry"))
por_municipio = (
    tabla.groupby("NOMB_MPIO")
    .size()
    .sort_values(ascending=False)
)

print("\nPARTE 2 - TOP 10 MUNICIPIOS")
print("Total de veredas:", len(gdf))
print(por_municipio.head(10).to_string())

# PARTE 3 - Calculo de areas
gdf_m = gdf.to_crs(epsg=9377)
gdf_m["area_ha"] = gdf_m.geometry.area / 10000

top5 = gdf_m.nlargest(5, "area_ha")

print("\nPARTE 3 - TOP 5 VEREDAS POR AREA")
print("CRS:", gdf_m.crs)
print(top5[
    ["NOMB_MPIO", "NOMBRE_VER", "area_ha"]
].round(2).to_string(index=False))

print("=" * 65)
print("EJERCICIO B1 FINALIZADO")
print("=" * 65)
