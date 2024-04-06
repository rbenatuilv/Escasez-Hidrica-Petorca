# Escasez-Hidrica-Petorca
Estudio de la escasez hídrica en la comuna de Petorca, región de Valparaíso. 

## Partes del trabajo

### `indexes.ipynb`

Contiene una explicación básica y las fórmulas de cada uno de los índices utilizados, junto a sus referencias.

### `test_image_splitting.py`

En este notebook se realiza la extracción de imágenes y datos, para luego generar una grilla fina y clasificada según uso del suelo en Petorca. Esto es con el objetivo de extraer imágenes de entrenamiento y calcular los índices indicadores de sequía para los diferentes tipos de zonas de la comuna, clasificadas en:

- Zona urbana
- Plantaciones
- Ríos
- Cuerpos de agua
- Otros

El resultado de esto permite medir la severidad de la sequía basado en datos satelitales. Además, las series de tiempo de cada índice permiten predecir el nivel de sequía esperado en un futuro.

### `PDSI.ipynb`

En este notebook se calcula el Palmer Severity Drought Index (PDSI) para medir el nivel de sequía de la comuna, basado en datos externos especializados para dicho fin. Además, las series de tiempo obtenidas de este índice también permiten realizar predicciones.

### `ResNETClassifiation`

En esta carpeta se encuentran los modelos basados en la arquitectura ResNET50 entrenados con las imágenes satelitales, de manera de clasificar el uso de suelo para las celdas de la grilla generada sobre las imágenes de estudio. Esto permite realizar una segmentación más específica de la zona, y más adaptable a los cambios que ocurren en esta. 

Lo anterior se puede utilizar para calcular la serie de tiempo de los indicadores de sequía (NDVI, NDWI, NMDI, PDSI) y poder realizar predicciones.

### `time_series_analysis`

Esta carpeta contiene los archivos `.R` que permiten analizar las series de tiempo extraídas con los métodos anteriores para realizar cálculos de tendencia y predicciones.

## Módulo `gee_objects.py`

La finalidad de la librería es agilizar la extracción de imágenes y valores de índices desde Google Earth Engine, tomando como input la región a estudiar como una GeoSeries.

### Funciones/Clases importantes

#### `GEERegion`

#####  `__init__(self, geometry: gpd.GeoSeries, name: str = 'GEERegion', crs: str = None)`

Método constructor del objeto `GEERegion`. Recibe la geometría de la región de estudio en formato `gpd.GeoSeries`. Opcionalmente, recibe el nombre de la región de estudio y el crs de la geometría ingresada (por defecto se extrae la propia de la geometría, pero al ingresar un nuevo crs se hace la transformación correspondiente).

##### `get_image(self, start_date: str | ee.Date, end_date: str | ee.Date, satt: str = 'Sentinel-2', clip: bool = False)`

Obtiene la imagen con menor cobertura de nubes de la región, entre las fechas `start_date` y `end_date`. Se puede especificar el satélite desde donde se extraerán las imágenes (por defecto Sentinel-2). El atributo clip permite obtener la imagen recortada según la geometría específica de la región. Si es `False` (por defecto), se toma la imagen que coincide con el `envelope` de la geometría de la región (se obtiene una imagen rectangular que contiene la región de interés).

##### `get_images(self, start_date: str | ee.Date, end_date: str | ee.Date, satt: str = 'Sentinel-2', dayfreq: int = 15, clip: bool = False)`

Extrae una serie de imágenes de la región entre las fechas `start_date` y `end_date` con frecuencia de `dayfreq` días. Es decir, extraerá una imagen cada `dayfreq` días desde la fecha `start_date` hasta la fecha `end_date`. El resto de atributos son análogos al método anterior.

##### `get_indexes(self, index_name: str, images: list[GEEImage] = None, start_date: str | ee.Date = None, end_date: str | ee.Date = None, satt='Sentinel-2', dayfreq=15, clip=False, add_bands: bool = False)`

Extrae una serie de imágenes con el tipo de índice especificado por `index_name`, proveniente de la lista de imágenes `images`. Opcionalmente, se pueden indicar las fechas de inicio y término de la extracción de imágenes, en vez de la lista de imágenes misma. En tal caso, se llamará al método anterior para obtener la lista correspondiente (con los argumentos descritos anteriormente) y luego se procederá a calcular el índice `index_name` para cada una de las imágenes.

Índices disponibles:
- NDVI: Normalized Difference Vegetation Index
- NDWI: Normalized Difference Water Index
- NMDI: Normalized Multi-Band Drought Index
- NDDI: Normalized Difference Drought Index (bajo revisión)

El argumento `add_bands` permite incorporar estos índices directamente como bandas a las imágenes proporcionadas.

##### `visualize(self, images: list[GEEImage], zoom=10, clip=False)`

Método para visualizar en `geemap` una lista de imágenes entregadas. Nuevamente, el atributo `clip` permite observar la geometría específica de la región. Si `clip = False` (default), se observará el `envelope` que contiene a la región (zona rectangular).


#### `GEEImage`

##### `__init__(self, image: ee.Image, satt: str, date: str, imgtype: str = 'all')`

Método constructor del objeto `GEEImage`. Funciona como un wrapping del objeto `ee.Image` y permite obtener de manera más sencilla la siguiente información (que recibe en el constructor):

- La imagen misma como objeto `ee.Image`.
- El nombre del satélite de la cual fue extraída.
- La fecha en la cual fue tomada la imagen.
- El tipo: `all` (default) si corresponde a una imagen con todas las bandas, (`ndvi`, `ndwi`, `nmdi`, `nddi`) si corresponde a una imagen de algún índice.

##### `clip(self, geometry: ee.Geometry)`

Este método permite recortar la `GEEImage` según la geometría proporcionada (análogo a `ee.Image.clip`).

##### `save(self, path: str = 'file.tif', format: str = 'GEO_TIFF', bands: list[str] = None)`

Este método permite guardar la imagen en formato `GEO_TIFF` o retornar un `numpy.array` con los valores de las bandas de la imagen. 
