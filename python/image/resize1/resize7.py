# -*- coding: utf-8 -*-
"""
Description: Get image size in pixels 
			 Resize 2 images to screen length [800]
			 width = scaled % of original width
"""

import PIL
from PIL import Image

file0 = "/home/antz/0_Python/image/Armadillo/img1.jpg"			# path to woring directory
file1 = "/home/antz/0_Python/image/Armadillo/img2.jpg"			# path for new images

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
	img.save('img3.jpg')
	
	baseheight = 1600
	img = Image.open(file1)
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img.save('img4.jpg')

if __name__ == "__main__": main()
