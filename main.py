from PIL import Image
import ImageProcessing
import serialCommunication
import os
from tkinter import filedialog
current_dir = os.path.dirname(os.path.abspath(__file__))
filearchivo=filedialog.askopenfilename(initialdir = current_dir,title = "Selecciona una imagen",filetypes = (("png files","*.png"),("jpg files","*.jpg"),("all files","*.*")))
img = Image.open(filearchivo)
imgpng=img.save(current_dir+'\\image.png')
ImageProcessing.process_image('image.png')
serialCommunication.printImage()