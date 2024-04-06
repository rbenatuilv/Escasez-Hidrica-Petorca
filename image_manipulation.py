from shapely import Polygon, MultiPolygon, to_geojson
import geopandas as gpd
import ee
from shapely.geometry import Polygon
import gee_objects as gee
import json


def make_geo_grid(geo: gpd.GeoSeries, n_pixels: int, pixel_res: int, crs='EPSG:32719'):

    box = geo.to_crs(crs)

    length = float((box.bounds['maxx'] - box.bounds['minx']).iloc[0])
    width = float((box.bounds['maxy'] - box.bounds['miny']).iloc[0])

    l_pixels = int(length / pixel_res)
    w_pixels = int(width / pixel_res)

    length_i = int(l_pixels / n_pixels)
    width_i = int(w_pixels / n_pixels)

    boxes = []

    for i in range(length_i):
        for j in range(width_i):
            x = i * n_pixels * pixel_res + float(box.bounds['minx'].iloc[0])
            y = j * n_pixels * pixel_res + float(box.bounds['miny'].iloc[0])
            box_ij = Polygon([(x, y), (x + n_pixels * pixel_res, y), 
                            (x + n_pixels * pixel_res, y + n_pixels * pixel_res), 
                            (x, y + n_pixels * pixel_res)])
            boxes.append(box_ij)

    boxes = gpd.GeoDataFrame(geometry=boxes, crs=crs)
    box = gpd.GeoDataFrame(geometry=box, crs=crs)

    grid = boxes[boxes.intersects(box.unary_union)].reset_index(drop=True)

    return grid


def make_ee_polygon(poly: Polygon):
    xx, yy = poly.exterior.coords.xy
    xy = [[xy[0], xy[1]] for xy in zip(xx,yy)]
    return ee.Geometry.Polygon(xy)


def make_ee_multi_polygon(multi_poly: MultiPolygon):
    geo_json = json.loads(to_geojson(multi_poly))

    return ee.Geometry.MultiPolygon(geo_json['coordinates'])


def image_splitter(image: gee.GEEImage, grid: gpd.GeoDataFrame, crs='EPSG:4326'):

    grid = grid.to_crs(crs)

    def divide(image, poly):
        poly = make_ee_polygon(poly)
        return image.clip(poly)

    divided = list(grid.geometry.apply(lambda x: divide(image.image, x)))

    return [gee.GEEImage(img, image.satt, image.date, tile_number=i) 
            for i, img in enumerate(divided)]


def get_index_median(image: gee.GEEImage, index: 'str', scale: int = 10):

    value = image.image.select(index).reduceRegion(**{
            'reducer': ee.Reducer.median(),
            'scale': scale,
            'maxPixels': 1e9
        }).getNumber(index).getInfo()
    
    return value