from gee_objects import GEEImage
import ee

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
            return result
        clusters = result.select('clusters')
        clusters = GEEImage(clusters, satt=image.satt, date=image.date, imgtype='clusters')
    
        return clusters