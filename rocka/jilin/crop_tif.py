from PIL import Image
from matplotlib import pyplot as plt

x = Image.open("jilin_rgb.tif")
# 1406 568
# y = x.crop((1406, 568, 1406 + 800, 568 + 1406))
y = x.crop((568, 1406, 2500 + 568, 1406 + 800))

y.save("jilin_rgb_2500x800.tif")
