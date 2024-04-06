from PIL import Image
from matplotlib import pyplot as plt
import rasterio
import os

name_tif = "./chunks/0-0.tif"
raster = rasterio.open(name_tif)
print(raster.transform)

# x = Image.open("jilin_rgb.tif")

# y = x.crop((568, 1406, 2500 + 568, 1406 + 800))

# y.save("jilin_rgb_2500x800.tif")

# with rasterio.open("jilin_rgb.tif") as src:
#     window = Window(col_off=568, row_off=1406, width=2500, height=800)

#     subset = src.read(window=window)

#     profile = src.profile

#     profile["width"], profile["height"] = window.width, window.height

#     profile["transform"] = rasterio.windows.transform(window, src.transform)

#     with rasterio.open("imagen_cortada.tif", "w", **profile) as dst:
#         dst.write(subset)
