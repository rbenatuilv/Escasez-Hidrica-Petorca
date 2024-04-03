SATT_INFO = {
        'Sentinel-2': {
            'URL': 'COPERNICUS/S2_SR_HARMONIZED',

            'frequency': 5,

            'scale': 1e-4,

            'offset': 0,

            'opt_bands': ['B2', 'B3', 'B4', 'B5', 'B6', 'B7', 'B8', 'B8A', 'B11', 'B12'],

            'qa_band': 'QA60',

            'cloud_masks': {
                'cloud_bit_mask': 1 << 10,
                'cirrus_bit_mask': 1 << 11
            },

            'indexes': {
                'NDVI': ['B8', 'B4'],
                'NDWI': ['B3', 'B8'],
                'NMDI': ['B8A', ('B11', 'B12')],
                'NDDI': ['NDVI', 'NDWI']
            },

            'visParams': {
                'rgb': {
                    'bands': ['B4', 'B3', 'B2'],
                    'min': 0.0,
                    'max': 0.3
                },
                'ndvi': {
                    'bands': ['NDVI'],
                    'min': -1,
                    'max': 1,
                    'palette': ['red', 'white', 'green']
                },
                'ndwi': {
                    'bands': ['NDWI'],
                    'min': -1,
                    'max': 1,
                    'palette': ['green', 'white', 'blue']
                },
                'nmdi': {
                    'bands': ['NMDI'],
                    'min': -1,
                    'max': 1,
                    'palette': ['green', 'white', 'brown']
                },
                'nddi': {
                    'bands': ['NDDI'],
                    'min': -1,
                    'max': 1,
                    'palette': ['red', 'white', 'green']
                },
                'clusters': {}
            }
        },

        'Landsat-8': {
            'URL': 'LANDSAT/LC08/C02/T1_L2',

            'frequency': 16,

            'scale': 2.75e-5,

            'offset': -0.2,

            'opt_bands': ['SR_B1', 'SR_B2', 'SR_B3', 'SR_B4', 'SR_B5', 'SR_B6', 'SR_B7'],

            'qa_band': 'QA_PIXEL',

            'cloud_masks': {
                'cloud_bit_mask': 1 << 3,
                'cirrus_bit_mask': 1 << 2,
                'cloud_shadow_bit_mask': 1 << 4
            },
            
            'indexes': {
                'NDVI': ['SR_B5', 'SR_B4'],
                'NDWI': ['SR_B3', 'SR_B5'],
                'NMDI': ['SR_B5', ('SR_B6', 'SR_B7')],  
                'NDDI': ['NDVI', 'NDWI']
            },

            'visParams': {
                'rgb': {
                    'bands': ['SR_B4', 'SR_B3', 'SR_B2'],
                    'min': 0.0,
                    'max': 0.3
                },
                'ndvi': {
                    'bands': ['NDVI'],
                    'min': -1,
                    'max': 1,
                    'palette': ['red', 'white', 'green']
                },
                'ndwi': {
                    'bands': ['NDWI'],
                    'min': -1,
                    'max': 1,
                    'palette': ['green', 'white', 'blue']
                },
                'nmdi': {
                    'bands': ['NMDI'],
                    'min': -1,
                    'max': 1,
                    'palette': ['green', 'white', 'brown']
                },
                'nddi': {
                    'bands': ['NDDI'],
                    'min': -1,
                    'max': 1,
                    'palette': ['red', 'white', 'green']
                },
                'clusters': {}
            }
        }
    }