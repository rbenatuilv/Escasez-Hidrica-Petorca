from tqdm import tqdm
import geopandas as gpd
import os
import image_manipulation as im
import gee_objects as gee
import pandas as pd
import ee


ee.Initialize()

crs_degree = 'EPSG:4326'


grid_urban = gpd.read_file(os.path.join('Data', 'grids', 'grid_urban.json'))
grid_plant = gpd.read_file(os.path.join('Data', 'grids', 'grid_plant.json'))
grid_agua = gpd.read_file(os.path.join('Data', 'grids', 'grid_agua.json'))
grid_rios = gpd.read_file(os.path.join('Data', 'grids', 'grid_rios.json'))
grid_others = gpd.read_file(os.path.join('Data', 'grids', 'grid_others.json'))


grids = {
    'urban': grid_urban,
    'plant': grid_plant,
    'agua': grid_agua,
    'rios': grid_rios,
    'otros': grid_others
}

petorca = gpd.read_file(os.path.join('Data', 'petorca.json'))

name = 'Petorca'
geo = petorca.geometry

satt = 'Landsat-8'
dates = ('2015-01-01', '2023-12-31')
day_freq = 30

region = gee.GEERegion(geo, name, crs_degree)

images = region.get_images(*dates, dayfreq=day_freq, satt=satt)

indexes = ['NDVI', 'NDWI', 'NMDI', 'NDDI']
indexes = {index: region.get_indexes(index, images, add_bands=True) for index in indexes}


print(grids.keys())
k = input()
keys = [k]
grids = {key: grids[key] for key in keys}


geometries = {key: im.make_ee_multi_polygon(grid.to_crs(crs_degree).geometry.unary_union) 
              for key, grid in tqdm(grids.items(), desc='Making geometries')}

columns = ['date', 'NDVI', 'NDWI', 'NMDI']

time_series = {
    key: {column: [] for column in columns}
    for key in grids.keys()
}

for img in tqdm(images, desc='Iterating over images'):
    for key, geo in geometries.items():
        time_series[key]['date'].append(img.date)

        img_clip = img.clip(geo)
        for index in columns[1:]:
            val = im.get_index_median(img_clip, index, scale=30)
            time_series[key][index].append(val)

for key, ts in time_series.items():
    ts = pd.DataFrame(ts)
    ts.to_excel(os.path.join('Data', f'{name}_{key}_time_series.xlsx'))
    print(f'{key} saved')
