from PIL import Image, ImageOps
import numpy as np

#https://github.com/mies47/MM-ordered_dithering

bayer8 = [
[0,48,12,60,3,51,15,63],
[32,16,44,28,35,19,47,31],
[8,56,4,52,11,59,7,55],
[40,24,36,20,43,27,39,23],
[2,50,14,62,1,49,13,61],
[34,18,46,30,33,17,45,29],
[10,58,6,54,9,57,5,53],
[42,26,38,22,41,25,37,21]]

def clampNumber(num, a, b):
    return min(max(num, a), b)

def process_image(src):
    image = Image.open(src)
    width, height = image.size
    dimensions = (160,144)
    img = np.array(ImageOps.fit(image, dimensions).convert("L"))
    x_max = np.size(img, axis=1)
    y_max = np.size(img, axis=0)

    #Loop through every pixel
    for x in range(x_max):
        for y in range(y_max):
            bayer = bayer8[y % 8][x % 8]
            c = img[y][x]
            c = clampNumber(c + ((bayer - 32) * 0.6), 0, 255)
            c = clampNumber(round(c / 64), 0, 3)

            img[y][x] = c * 64

    image = Image.fromarray(img).convert('L').resize((x_max * 10,y_max * 10),resample=Image.NEAREST)
    image.save('dithered.png', bit=2)