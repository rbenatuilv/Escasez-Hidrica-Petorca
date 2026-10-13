**Español** | [English](README.md)

# Escasez hídrica en Petorca — Monitoreo de sequía con datos satelitales

Proyecto en equipo (2024) que estudia la **sequía y escasez hídrica en Petorca**, comuna
de la Región de Valparaíso conocida por su crisis hídrica y sus plantaciones de paltos.
Usa imágenes Sentinel-2 y Landsat-8, obtenidas mediante **Google Earth Engine**, para:

1. dividir la comuna en una grilla fina y clasificar cada celda según uso de suelo;
2. calcular índices de vegetación y sequía (NDVI, NDWI, NMDI, PDSI) para cada tipo de uso
   de suelo a lo largo del tiempo;
3. analizar las series de tiempo resultantes para estimar tendencias y hacer predicciones.

<p align="center">
  <img src="Data/grid_image.png" width="48%" alt="Grilla de Petorca clasificada por uso de suelo">
  <img src="Data/NDVI_graph.png" width="48%" alt="Series de tiempo de NDVI por uso de suelo">
</p>

## Flujo de trabajo

### 1. Grilla de uso de suelo — [`test_image_splitting.ipynb`](test_image_splitting.ipynb)
Se combinan el límite comunal (Biblioteca del Congreso Nacional), los polígonos de
plantaciones de paltos del CIREN, la hidrografía y las zonas urbanas para dividir Petorca
en una grilla. Cada celda se clasifica como **zona urbana**, **plantación**, **río**,
**cuerpo de agua** u **otro** ([`image_manipulation.py`](image_manipulation.py)). La grilla
se usa tanto para extraer imágenes de entrenamiento como para agregar los índices por tipo
de uso de suelo.

### 2. Índices de sequía — [`indexes.ipynb`](indexes.ipynb), [`time_series.py`](time_series.py), [`PDSI.ipynb`](PDSI.ipynb)
- `indexes.ipynb` documenta las fórmulas de cada índice para Sentinel-2 y Landsat-8, con
  sus referencias.
- `time_series.py` calcula la mediana de NDVI / NDWI / NMDI de cada tipo de uso de suelo
  sobre imágenes mensuales de Landsat-8 (2015–2023) y exporta las series a
  `Data/Petorca_*_time_series.xlsx`.
- `PDSI.ipynb` usa datos de TerraClimate para analizar el Palmer Drought Severity Index
  (PDSI) junto con la evapotranspiración potencial y real (PET, AET) y la escorrentía (RO).

### 3. Clasificación de uso de suelo — [`ResNETClassification/`](ResNETClassification), [`model_train.ipynb`](model_train.ipynb)
- Se hace *fine-tuning* de una **ResNet-50** sobre el dataset
  [EuroSAT](https://github.com/phelber/EuroSAT) (`OE1_fineTuneModels.ipynb`, Google Colab).
  Luego se usa para clasificar las celdas Sentinel-2 de Petorca entre 2018 y 2023
  (`OE2_ClasificacionLULC_S2.ipynb`), lo que permite seguir los cambios de uso de suelo en
  el tiempo.
- Como alternativa más liviana, `model_train.ipynb` entrena clasificadores Random Forest y
  SVM sobre imágenes de Petorca etiquetadas a mano (`Data/PetorcaSAT/`: built, crop, grass,
  water), con rebalanceo SMOTE-Tomek.
- [`segment.py`](segment.py) implementa segmentación en superpíxeles SNIC y vectorización
  mediante Earth Engine.

### 4. Análisis de series de tiempo — [`time_series_analysis/`](time_series_analysis)
Scripts de R, uno por tipo de uso de suelo, que ajustan una regresión armónica
(estacionalidad), una tendencia lineal y modelos ARIMA a las series de NDVI, para
cuantificar la tendencia y predecir niveles de sequía. [`Time_Series.R`](Time_Series.R)
aplica el mismo análisis a la comuna completa.

## `gee_objects.py` — Módulo auxiliar para Earth Engine

Una librería pequeña que agiliza la extracción de imágenes y valores de índices desde
Google Earth Engine para cualquier región entregada como geometría de GeoPandas. Los
parámetros propios de cada satélite (bandas, factores de escala, máscaras de nubes) están
en [`sat_params.py`](sat_params.py).

```python
import ee, geopandas as gpd
import gee_objects as gee

ee.Initialize()
geometry = gpd.read_file('Data/petorca.json').geometry
petorca = gee.GEERegion(geometry, name='Petorca', crs='EPSG:4326')

images = petorca.get_images('2023-01-01', '2023-12-31', satt='Sentinel-2', dayfreq=15)
ndvi   = petorca.get_indexes('NDVI', images=images)
petorca.visualize(ndvi)
```

### `GEERegion(geometry, name='GEERegion', crs=None)`
La región de estudio. Recibe un `gpd.GeoSeries`; si se entrega `crs`, la geometría se
transforma a ese sistema de referencia.

| Método | Descripción |
|---|---|
| `get_image(start_date, end_date, satt='Sentinel-2', clip=False)` | Imagen con menor nubosidad de la región entre dos fechas. Con `clip=False` la imagen cubre el rectángulo envolvente de la región; con `clip=True` se recorta a la geometría exacta. |
| `get_images(start_date, end_date, satt='Sentinel-2', dayfreq=15, clip=False)` | Una imagen cada `dayfreq` días entre las dos fechas. |
| `get_indexes(index_name, images=None, start_date=None, end_date=None, satt='Sentinel-2', dayfreq=15, clip=False, add_bands=False)` | Calcula un índice para una lista de imágenes, o primero obtiene las imágenes si se entregan fechas. Índices disponibles: **NDVI**, **NDWI**, **NMDI** y NDDI (experimental). Con `add_bands=True` el índice se agrega como banda a las imágenes originales. |
| `visualize(images, zoom=10, clip=False)` | Muestra las imágenes en un mapa interactivo de `geemap`. |

### `GEEImage(image, satt, date, imgtype='all')`
Un *wrapper* de `ee.Image` que guarda el satélite, la fecha de captura y el tipo de imagen
(`all` para todas las bandas, o el nombre de un índice).

| Método | Descripción |
|---|---|
| `clip(geometry)` | Recorta la imagen según una `ee.Geometry`. |
| `save(path='file.tif', format='GEO_TIFF', bands=None)` | Guarda la imagen como GeoTIFF, o retorna los valores de las bandas como un arreglo de `numpy`. |

## Estructura del repositorio

```
gee_objects.py, sat_params.py   # Wrapper de Earth Engine y parámetros satelitales
image_manipulation.py           # Creación de grillas y división de imágenes
segment.py                      # Segmentación SNIC
time_series.py                  # Extracción de series de índices por uso de suelo
*.ipynb                         # Notebooks de análisis (ver Flujo de trabajo)
ResNETClassification/           # Modelos ResNet-50, notebooks y predicciones
time_series_analysis/           # Modelos de series de tiempo en R por uso de suelo
auxiliars/                      # Auxiliar de visualización con Folium/Earth Engine
Data/                           # Límites, grillas, imágenes etiquetadas y series exportadas
```

## Requisitos

- Python 3.10+ con `earthengine-api`, `geemap`, `geopandas`, `pandas`, `numpy`,
  `matplotlib`, `tqdm` y `scikit-learn`; `torch` / `torchvision` para los notebooks de
  ResNet.
- Una cuenta de Google Earth Engine (`earthengine authenticate`).
- R con `forecast` y `TTR` para los scripts de series de tiempo.

## Equipo

- [@rbenatuilv](https://github.com/rbenatuilv)
- [@minsoos](https://github.com/minsoos)
- [@lfcpardo](https://github.com/lfcpardo)
