
from PIL import Image
import numpy
import os

imagesize = (81, 81)

im2 = Image.new('RGBA', imagesize)

for x in range(imagesize[0]):
    for y in range(imagesize[1]):
        im2.putpixel((x,y),(100,255,1,0))

im2.save('noize.jpg')
