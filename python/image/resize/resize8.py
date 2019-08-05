# -*- coding: utf-8 -*-
"""
Description: Get image size in pixels 
			 Resize 2 images to screen heightxwidth
			 [800x408] even if image is distorted
"""

import PIL
from PIL import Image

file0 = 'img1.jpg'
file1 = 'img2.jpg'

def main():
	# Get image pixel size (width x height)
	with Image.open(file0) as img:
		width, height = img.size
	print('{0}, {1}'.format(width, height))
	
	basewidth = 800
	hsize = 480
	img = Image.open(file0)
	#wpercent = (basewidth / float(img.size[0]))
	#hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img.save('img3.jpg')
	
	baseheight = 800
	hsize = 480
	img = Image.open(file1)
	#wpercent = (basewidth / float(img.size[0]))
	#hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img.save('img4.jpg')

if __name__ == "__main__": main()
