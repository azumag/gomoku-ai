import sys
import common.util as u
from PIL import Image

util = u.Util()

input_d = sys.argv[1]
label_d = sys.argv[2]

imagesize = (9, 9)

train_data  = util.load_data(input_d)
train_label = util.load_data(label_d)

count = 0

train_txt = ''

for trda in train_data:
    label = train_label[count].index(1) # one-hot
    im2 = Image.new('RGBA', imagesize)
    for x in range(imagesize[0]):
        for y in range(imagesize[1]):
            cell = trda[x*imagesize[0]+y]
            if cell == 0:
                im2.putpixel((x,y),(255,0,0,0))
            elif cell == 1:
                im2.putpixel((x,y),(0,255,0,0))
            elif cell == 2:
                im2.putpixel((x,y),(0,0,255,0))
            else:
                print cell
                print 'unknown errr'
    filename = 'board_img/'+str(count)+'.bmp'
    im2.save(filename)
    train_buffer = filename + ' ' + str(label) + '\n'
    f = open('train.txt', 'a')
    f.write(train_buffer)
    f.close()
    count += 1
