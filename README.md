# Escasez-Hidrica-Petorca
Estudio de la escasez hídrica en la comuna de Petorca, región de Valparaíso. 


## Módulo `gee_objects.py`

La finalidad de la librería es agilizar la extracción de imágenes y valores de índices desde Google Earth Engine, tomando como input la región a estudiar como una GeoSeries.

### Funciones/Clases importantes

#### `GEERegion`

#####  `__init__(self, geometry: gpd.GeoSeries, name: str = 'GEERegion', crs: str = None)`

Método constructor del objeto `GEERegion`. Recibe la geometría de la región de estudio en formato `gpd.GeoSeries`. Opcionalmente, recibe el nombre de la región de estudio y el crs de la geometría ingresada (por defecto se extrae la propia de la geometría, pero al ingresar un nuevo crs se hace la transformación correspondiente).

##### `get_image(self, start_date: str | ee.Date, end_date: str | ee.Date, satt: str = 'Sentinel-2', clip: bool = False)`

Obtiene la imagen con menor cobertura de nubes de la región, entre las fechas `start_date` y `end_date`. Se puede estecificar el satélite desde donde se extraerán las imágenes (por defecto Sentinel-2). El atributo clip permite obtener la imagen recortada según la geometría específica de la región. Si es `False` (por defecto), se toma la imagen que coincide con el `envelope` de la geometría de la región (se obtiene una imagen rectangular que contiene la región de interés).

##### `get_images(self, start_date: str | ee.Date, end_date: str | ee.Date, satt: str = 'Sentinel-2', dayfreq: int = 15, clip: bool = False)`

Extrae una serie de imágenes de la región entre las fechas `start_date` y `end_date` con frecuencia de `dayfreq` días. Es decir, extraerá una imagen cada `dayfreq` días desde la fecha `start_date` hasta la fecha `end_date`. El resto de atributos son análogos al método anterior.

##### `get_indexes(self, index_name: str, images: list[GEEImage] = None, start_date: str | ee.Date = None, end_date: str | ee.Date = None, satt='Sentinel-2', dayfreq=15, clip=False)`

Extrae una serie de imágenes con el tipo de índice especificado por `index_name`, proveniente de la lista de imágenes `images`. Opcionalmente, se pueden indicar las fechas de inicio y término de la extnacción de imágenes, en vez de la lista de imágenes misma. En tal caso, se llamará al método anterior para obtener la lista correspondiente (con los argumentos descritos anteriormente) y luego se pdocederá a calcular el índice `index_name` para cada una de las imágenes.

Índices disponibles:
- NDVI: Normalized Difference Vegetation Index
- NDWI: Normalized Difference Water Index
- NMDI: Normalized Multi-Band Drought Index
- NDDI: Normalized Difference Drought Index (bajo revisión)

##### visualize(self, images: list[GEEImage], zoom=10, clip=False)

Método para visualizar en `geemap` una lista de imágenes entregadas. Nuevamente, el atributo `clip` permite observar la geometría específica de la región. Si `clip = False` (default), se observará el `envelope` que contiene a la región (zona rectangular).