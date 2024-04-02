import ee
import geemap
import geopandas as gpd
from sat_params import SATT_PARAMS


class GEEImage:
    """
    Class that represents an image from Google Earth Engine.
    """

    def __init__(self, image: ee.Image, satt: str, date: str, 
                 imgtype: str = 'all'):
        self.image = image
        self.satt = satt
        self.date = date
        self.img_type = imgtype


class GEERegion:
    """
    Class that represents a region of interest for Google Earth Engine.
    """

    SATT_INFO = SATT_PARAMS


    def __init__(self, geometry: gpd.GeoSeries, name: str = 'GEERegion', crs: str = None):
        self.name = name
        self.geometry = geometry

        if crs is None:
            crs = geometry.crs
        else:
            self.geometry = geometry.to_crs(crs)

        self.crs = crs
        self.center = self.get_ee_center()

    def to_crs(self, crs):
        """
        Modifies the crs of the region and updates the center.
        """
        
        self.geometry = self.geometry.to_crs(crs)
        self.crs = crs
        self.center = self.get_ee_center()

    def get_ee_geometry(self, envelope=True):
        """
        Obtains the geometry of the region as an ee.Geometry.Polygon object.
        """

        if envelope:
            geometry = self.geometry.unary_union.envelope
        else:
            geometry = self.geometry.unary_union
        xx, yy = geometry.exterior.coords.xy
        xy = [[xy[0], xy[1]] for xy in zip(xx,yy)]
        return ee.Geometry.Polygon(xy)
    
    def get_ee_center(self):
        """
        Obtains the center of the region as an ee.Geometry.Point object.
        """

        geo = self.geometry.unary_union
        coords = [geo.centroid.x, geo.centroid.y]
        return ee.Geometry.Point(coords)
    
    def apply_scale_factors(self, image, opt_bands, scale, offset):
        """
        Applies the scale factors to the specified bands of the image.
        """

        optical_bands = image.select(opt_bands).multiply(scale).add(offset)
        return image.addBands(optical_bands, None, True)
    
    def mask_clouds(self, image, qa_band, masks):
        """
        Masks the clouds in the image using the specified QA band and masks.
        """
  
        qa = image.select(qa_band)

        mask = qa.bitwiseAnd(masks[0]).eq(0)
        for m in masks[1:]:
            mask = mask.And(qa.bitwiseAnd(m).eq(0))

        return image.updateMask(mask)

    def get_image(self, start_date: str | ee.Date, end_date: str | ee.Date, 
                  satt='Sentinel-2', clip=False):
        """
        Obtains the least cloudy image from the specified satellite (default: Sentinel-2) 
        between the specified dates.
        """

        geo = self.get_ee_geometry(envelope = not clip)

        collection = ee.ImageCollection(self.SATT_INFO[satt]['URL']).filterBounds(self.center)
        collection = collection.filterDate(start_date, end_date)

        image = ee.Image(collection.sort('CLOUDY_PIXEL_PERCENTAGE').first()).clip(geo)

        image = self.mask_clouds(image, self.SATT_INFO[satt]['qa_band'], 
                                 list(self.SATT_INFO[satt]['cloud_masks'].values()))

        image = self.apply_scale_factors(image, self.SATT_INFO[satt]['opt_bands'], 
                                         self.SATT_INFO[satt]['scale'], self.SATT_INFO[satt]['offset'])

        image_date = ee.Date(image.get('system:time_start')).format('YYYY-MM-dd').getInfo()

        return GEEImage(image, satt, image_date)

    def get_images(self, start_date: str | ee.Date, end_date: str | ee.Date, 
                   satt='Sentinel-2', dayfreq=15, clip=False):
        """
        Obtains a list of images from the specified satellite (default: Sentinel-2)
        between the specified dates with the specified frequency.
        """

        start_date = ee.Date(start_date)
        end_date = ee.Date(end_date)

        sat_freq = self.SATT_INFO[satt]['frequency']

        if dayfreq < sat_freq:
            raise ValueError(f'Frequency must be greater than {self.SATT_INFO[satt]["frequency"]} days.')
        
        diff = end_date.difference(start_date, 'day').round().getInfo()

        if diff < dayfreq:
            raise ValueError('The difference between dates must be greater than the frequency.')
        
        dates = [start_date.advance(i, 'day') for i in range(0, diff + 1, dayfreq)]
        if end_date.difference(dates[-1], 'day').getInfo() > max(dayfreq // 2, sat_freq):
            dates.append(end_date)

        images = [self.get_image(dates[i], dates[i + 1], satt, clip) for i in range(len(dates) - 1)]

        return images

    def get_ndvi(self, image: GEEImage):
        """
        Obtains the NDVI index of the specified image.
        """

        indexes = self.SATT_INFO[image.satt]['indexes']['NDVI']
        ndvi = image.image.normalizedDifference(indexes).rename('NDVI')
        return GEEImage(ndvi, image.satt, image.date, 'ndvi')

    def get_ndwi(self, image: GEEImage):
        """
        Obtains the NDWI index of the specified image.
        """

        indexes = self.SATT_INFO[image.satt]['indexes']['NDWI']
        ndwi = image.image.normalizedDifference(indexes).rename('NDWI')
        return GEEImage(ndwi, image.satt, image.date, 'ndwi')
    
    def get_nmdi(self, image: GEEImage):
        """
        Obtains the NMDI index of the specified image.
        """

        indexes = self.SATT_INFO[image.satt]['indexes']['NMDI']
        img = image.image

        swirdiff = img.select(indexes[1][0]).subtract(img.select(indexes[1][1])).rename('SWIR-DIFF')
        img = img.addBands(swirdiff)
        nmdi = img.normalizedDifference([indexes[0], 'SWIR-DIFF']).rename('NMDI')

        return GEEImage(nmdi, image.satt, image.date, 'nmdi')
    
    def get_nddi(self, image: GEEImage):
        """
        Obtains the NDDI index of the specified image.
        """

        ndvi = self.get_ndvi(image).image
        ndwi = self.get_ndwi(image).image

        nddi = ndvi.subtract(ndwi).divide(ndvi.add(ndwi)).rename('NDDI')

        return GEEImage(nddi, image.satt, image.date, 'nddi')
    
    def get_indexes(self, index_name: str, images: list[GEEImage] = None, start_date: str | ee.Date = None,
                    end_date: str | ee.Date = None, satt='Sentinel-2', dayfreq=15, clip=False):
        """
        Obtains the specified index of the specified images.
        """
        index_dict = {
            'NDVI': self.get_ndvi,
            'NDWI': self.get_ndwi,
            'NMDI': self.get_nmdi,
            'NDDI': self.get_nddi
        }

        try:
            index_dict[index_name]
        except KeyError:
            raise ValueError('Invalid index name. Indexes available: NDVI, NDWI, NMDI, NDDI.')

        if images is None:
            if start_date is None or end_date is None:
                raise ValueError('Either images or start_date and end_date must be specified.')

            images = self.get_images(start_date, end_date, satt, dayfreq, clip)
        
        indexes = [index_dict[index_name](image) for image in images]

        return indexes
    
    def visualize(self, images: list[GEEImage], zoom=10, clip=False):
        """
        Visualizes the image in the specified mode (default: rgb)
        using geemap. The title of the map can be specified (default: map).
        """
        modes = {
            'all': 'rgb',
            'rgb': 'rgb',
            'ndvi': 'ndvi',
            'ndwi': 'ndwi',
            'nmdi': 'nmdi',
            'nddi': 'nddi'
        }

        m = geemap.Map()
        m.centerObject(self.center, zoom)

        show = True
        for image in images:
            params = self.SATT_INFO[image.satt]['visParams'][modes[image.img_type]]
            title = f'{self.name} {modes[image.img_type].upper()} {image.date}'

            if clip:
                m.addLayer(image.image.clip(self.get_ee_geometry(envelope=False)), 
                           params, title, shown=show)
            else:
                m.addLayer(image.image, params, title, shown=show)
            show = False

        return m
