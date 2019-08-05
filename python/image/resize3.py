# -*- coding: utf-8 -*-
"""
Description: Get image size in pixels 
			 Resize 2 other images
			 Save them to working directory
"""

import PIL
from PIL import Image

file0 = '/home/antz/0_CV3/pics/gr5.jpg'

def main():
	# Get image pixel size (width x height)
	with Image.open(file0) as img:
		width, height = img.size
	print('{0}, {1}'.format(width, height))
	
	basewidth = 560
	img = Image.open('pics/gr5.jpg')
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img.save('resized_image1.jpg')
	
	baseheight = 560
	img = Image.open('pics/gr7.jpg')
	hpercent = (baseheight / float(img.size[1]))
	wsize = int((float(img.size[0]) * float(hpercent)))
	img = img.resize((wsize, baseheight), PIL.Image.ANTIALIAS)
	img.save('resized_image2.jpg')

if __name__ == "__main__": main()
