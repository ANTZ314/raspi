# -*- coding: utf-8 -*-
"""
Description: Get image size in pixels 
			 Resize 1 by image width
			 Resize 1 by image height
			 Save each resized image
"""
import PIL
from PIL import Image

file0 = '/home/antz/0_Python/image/img1.jpg'
file1 = '/home/antz/0_Python/image/img2.jpg'

def main():
	# Get image pixel size (width x height)
	with Image.open(file0) as img:
		width, height = img.size
	print('{0}, {1}'.format(width, height))
	
	basewidth = 1600
	img = Image.open(file0)
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img.save('resized_image1.jpg')
	
	baseheight = 1600
	img = Image.open(file1)
	hpercent = (baseheight / float(img.size[1]))
	wsize = int((float(img.size[0]) * float(hpercent)))
	img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
	img.save('resized_image2.jpg')

if __name__ == "__main__": main()
