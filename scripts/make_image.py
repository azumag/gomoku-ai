from PIL import Image
import numpy
import os
import sys

imagesize = (9, 9)

name = sys.argv[1]
input_d = sys.argv[2:]


im2 = Image.new('RGBA', imagesize)

for x in range(imagesize[0]):
    for y in range(imagesize[1]):
        cell = input_d[x*imagesize[0]+y]
        if cell == '0':
            im2.putpixel((x,y),(255,0,0,0))
        elif cell == '1':
            im2.putpixel((x,y),(0,255,0,0))
        elif cell == '2':
            im2.putpixel((x,y),(0,0,255,0))
        else:
            print 'unknown errr'

im2.save(name+'.bmp')
