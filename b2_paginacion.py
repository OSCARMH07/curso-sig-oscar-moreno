# B2 - APIs y paginacion
# Autor: Oscar Moreno Hoyos

import requests

url = (
    "https://services6.arcgis.com/Ex2fmFOuTOHRZtML/"
    "ArcGIS/rest/services/Veredas_Boyaca_2024/"
    "FeatureServer/0/query"
)

base = {
    "where": "COD_DPTO=15",
    "outFields": "NOMB_MPIO,NOMBRE_VER",
    "outSR": "4326",
    "f": "geojson"
}

def paginar(bloque):
    features = []
    offset = 0
    vueltas = 0

    print("\nTAMANO DEL BLOQUE:", bloque)
    print("-" * 55)

    while True:
        p = {
            **base,
            "resultOffset": offset,
            "resultRecordCount": bloque
        }

        r = requests.get(url, params=p, timeout=120)
        r.raise_for_status()
        datos = r.json()

        if "error" in datos:
            raise RuntimeError(datos["error"])

        nuevos = datos["features"]
        features += nuevos
        vueltas += 1

        print(
            f"Offset {offset}: +{len(nuevos)} "
            f"(total {len(features)})"
        )

        if len(nuevos) < bloque:
            break

        offset += bloque

    municipios = {
        f["properties"]["NOMB_MPIO"]
        for f in features
        if f["properties"]["NOMB_MPIO"]
    }

    print("TOTAL VEREDAS:", len(features))
    print("MUNICIPIOS DISTINTOS:", len(municipios))
    print("VUELTAS DEL BUCLE:", vueltas)

    return len(features), municipios

print("=" * 55)
print("B2 - CONSUMO DE APIs Y PAGINACION")
print("=" * 55)

total1000, municipios1000 = paginar(1000)
total500, municipios500 = paginar(500)

print("\nCOMPARACION DE RESULTADOS")
print("-" * 55)
print("Total con bloques de 1000:", total1000)
print("Total con bloques de 500:", total500)
print("Mismo total:", total1000 == total500)
print("Mismos municipios:", municipios1000 == municipios500)
print("Total filtrado verificado 1712:", total1000 == total500 == 1712)
print("=" * 55)



