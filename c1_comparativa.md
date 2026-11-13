# C1 — Repaso de estándares con servicios reales

**Estudiante:** Oscar Moreno Hoyos  
**Curso:** Servicios SIG y Sitios Web — Maestría en SIG  
**Fecha de consulta:** 13 de noviembre de 2026

## 1. WMS del DANE — MGN 2024

Se consultó la operación `GetCapabilities` del servicio WMS del Marco Geoestadístico Nacional 2024. La respuesta HTTP fue 200 y el documento XML indicó la versión 1.3.0.

**¿Cuántas capas publica?** 10 capas con nombre, identificadas dentro de 11 nodos `Layer` (incluido el contenedor principal).

| Identificador | Capa |
|---|---|
| 0 | Manzana |
| 1 | Sección Urbana |
| 2 | Sector Urbano |
| 3 | Sección Rural |
| 4 | Sector Rural |
| 5 | Clase |
| 6 | Zona Urbana |
| 7 | Municipio |
| 8 | Departamento |
| 9 | País |

**¿Qué CRS soporta?** Los identificadores anunciados en el XML son `CRS:84`, `EPSG:102100`, `EPSG:3857` y `EPSG:4326`. Se conservan tal como aparecen en la respuesta del servicio.

Los formatos de salida de `GetMap` son `image/bmp`, `image/jpeg`, `image/tiff`, `image/png`, `image/png8`, `image/png24`, `image/png32`, `image/gif` e `image/svg+xml`.

[Consulta GetCapabilities del DANE](https://geoportal.dane.gov.co/mparcgis/services/MGN2024/Serv_CapasMGN_2024/MapServer/WMSServer?service=WMS&request=GetCapabilities)

## 2. Comparación de las respuestas JSON

### FeatureServer (Esri) — Veredas de Boyacá

Se ejecutó la consulta con `where=1=1`, `outFields=*`, `resultRecordCount=3` y `f=geojson`. La respuesta contiene tres entidades de tipo `Polygon`, todas del municipio de Tunja.

| ID | NOMBRE_VER | NOMB_MPIO | CODIGO_VER |
|---|---|---|---|
| 1 | LA LAJITA | TUNJA | 15001004 |
| 2 | LA HOYA | TUNJA | 15001003 |
| 3 | BARON | TUNJA | 15001000 |

[Consulta de tres veredas](https://services6.arcgis.com/Ex2fmFOuTOHRZtML/ArcGIS/rest/services/Veredas_Boyaca_2024/FeatureServer/0/query?where=1%3D1&outFields=*&resultRecordCount=3&f=geojson)

### OGC API Features — demo pygeoapi

Se consultó el catálogo de colecciones y se seleccionó `obs` (Observations). Con `limit=3` y `f=json` se obtuvieron tres entidades de tipo `Point`.

| ID | stn_id | datetime (UTC) | value |
|---|---|---|---|
| 371 | 35 | 2001-10-30T14:24:55Z | 89.9 |
| 377 | 35 | 2002-10-30T18:31:38Z | 93.9 |
| 238 | 2147 | 2007-10-30T08:57:29Z | 103.5 |

[Catálogo pygeoapi](https://demo.pygeoapi.io/master/collections?f=json) · [Consulta de tres observaciones](https://demo.pygeoapi.io/master/collections/obs/items?limit=3&f=json)

### Diferencias y similitudes observadas

| Elemento | FeatureServer | OGC API Features (pygeoapi) |
|---|---|---|
| Tipo de respuesta | `FeatureCollection` | `FeatureCollection` |
| Entidades devueltas | 3 | 3 |
| Estructura de cada entidad | `type`, `id`, `geometry`, `properties` | `type`, `id`, `geometry`, `properties` |
| Geometría de la muestra | `Polygon` | `Point` |
| Tipo de `id` de la entidad | Numérico | Cadena de texto |
| Campos de atributos | 34; incluyen `NOMBRE_VER`, `NOMB_MPIO`, `CODIGO_VER` | 4: `id`, `stn_id`, `datetime`, `value` |
| Límite solicitado | `resultRecordCount=3` | `limit=3` |
| Total de coincidencias | No informado en esta respuesta | `numberMatched: 5` |
| Cantidad devuelta como metadato | No informado explícitamente | `numberReturned: 3` |
| Paginación | `properties.exceededTransferLimit: true` indica más resultados | `links` contiene `rel: next`, cuya URL incluye `offset=3` |
| Enlaces de navegación | No aparecen en esta respuesta | `self`, `alternate`, `next`, `collection` |

Ambos servicios entregan datos vectoriales con geometrías y atributos en GeoJSON. Las diferencias de geometría y atributos se deben a las colecciones consultadas. La diferencia en paginación es que FeatureServer señala que existen más resultados mediante `exceededTransferLimit`, mientras que pygeoapi incluye un enlace para continuar la consulta.

## 3. Tabla comparativa de estándares

| Servicio | Qué entrega | Cómo se filtra | Cómo se pagina |
|---|---|---|---|
| WMS | Mapas renderizados, por ejemplo PNG o JPEG, mediante `GetMap`. `GetCapabilities` describe el servicio. | Selección de capas (`LAYERS`) y extensión espacial (`BBOX`); se especifica el CRS y el estilo de representación. | No aplica paginación de entidades a `GetMap`; se solicitan imágenes para distintas extensiones. |
| WFS | Entidades vectoriales con geometrías y atributos mediante `GetFeature`, generalmente GML; otros formatos según el servidor. | `BBOX` para extensión espacial y filtros OGC (`FILTER`) para condiciones espaciales o de atributos. | En WFS 2.0, `startIndex` y `count`. En versiones anteriores, `maxFeatures` limita los resultados. |
| FeatureServer (Esri) | Entidades vectoriales en JSON o GeoJSON mediante `/query`. | `where` para atributos, `geometry` y `spatialRel` para relaciones espaciales. `outFields` selecciona los campos devueltos. | `resultOffset` y `resultRecordCount` cuando el servicio admite paginación; `exceededTransferLimit` ayuda a identificar si quedan resultados. |
| OGC API Features | Entidades vectoriales a través de `/collections/{id}/items`, por ejemplo en GeoJSON. | `bbox` para extensión espacial y `datetime` para tiempo; otros filtros dependen de las capacidades del servicio. | `limit` controla el tamaño de página; se sigue el enlace `next` cuando está disponible. En la demo consultada este enlace usa `offset`. |

WMS y WFS corresponden a servicios OGC clásicos que utilizan operaciones y parámetros de consulta; FeatureServer y OGC API Features permiten consultar recursos por rutas REST. WMS se orienta a la representación cartográfica, mientras que los otros tres servicios permiten recuperar entidades vectoriales para su procesamiento.

