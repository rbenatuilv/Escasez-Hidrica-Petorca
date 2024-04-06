from gee_objects import GEEImage
import ee
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, Polygon

class Snic:
    def __init__(self, size: int, compactness: int, connectivity: int, crs: str):
        '''
        Snic segmentation use seed points so it could generate regions based in compactness and connectivity
        Size represent the space between each seed
        '''
        if not connectivity in [4, 8]:
            raise ValueError("Connectivity must be 4 or 8") 
        self.size = size
        self.compact = compactness
        self.connec = connectivity
        self.crs = f"epsg:{crs}"
    
    def run(self, image: GEEImage, returnbands: bool=False):
        '''
        Run snic algorithm. 
        addbands variable appends segmentation bands to the original image.
        Bands included are mean of each band and clusters.
        '''
        if image.satt == 'Landsat-8':
            scale = 30
        elif image.satt == 'Sentinel-2':
            scale = 20
        else:
            raise TypeError("Unknown sattelite")
        snic_alg = ee.Algorithms.Image.Segmentation.SNIC
        result = snic_alg(image.image, size=self.size, compactness=self.compact, 
                  connectivity=self.connec).reproject(crs=self.crs, scale=scale)
        if returnbands:
            result = GEEImage(result, satt=image.satt, date=image.date, imgtype='rgb mean')
            return result
        clusters = result.select('clusters')
        clusters = GEEImage(clusters, satt=image.satt, date=image.date, imgtype='clusters')
    
        return clusters
    
    def vectorization(self, image: GEEImage, bands: list, geobounds: Polygon, crs: str=None):
        if crs == None:
            crs = self.crs
        vectors = image.image.select(*bands).reduceToVectors(
            geometry= image.image.geometry(),
            crs= crs,
            scale=30,
            geometryType= 'polygon',
            eightConnected= False,
            labelProperty= 'clusters',
            reducer= ee.Reducer.min(),
            bestEffort=True,
            tileScale=16
            )
        vec_list = vectors.toList(100000)
        df = pd.DataFrame(vec_list.getInfo())
        df = pd.concat([df.drop(['properties'], axis=1), df['properties'].apply(pd.Series)], axis=1)
        df = pd.concat([df.drop(['geometry'], axis=1), df['geometry'].apply(lambda x: Polygon(x['coordinates'][0]))], axis=1)
        df = df.drop(['type', 'id'], axis=1)
        geo_df = gpd.GeoDataFrame(df, geometry='geometry', crs=crs)
        geo_df = geo_df.clip(geobounds)
        geo_df = geo_df.dissolve(by='clusters', aggfunc='mean')
        print("segments figure:", len(geo_df))
        return geo_df
