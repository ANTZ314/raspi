# -*- coding: utf-8 -*-
"""
Description: Get number of files in 'pics' folder
			 Check each pixel size
			 If larger than 480 x 320
			 Resize to ? (size of Pi Cam image)
"""
import PIL
from PIL import Image
import os
import shutil

file0 = '../pics/'
file1 = 'resized_4.jpg'
dest = '/home/antz/0Python/image/size'
images = 0			# number of images
sizeW = 0			# pixel width of images
cnt = 0				# generic counter
incr = 0			# resized image counter

def fcount(path):
	count = 0
	for f in os.listdir(file0):
		if os.path.isfile(os.path.join(path, f)):
			count += 1
	return count
	
def No_images():
	Image_No = 0
	Image_No = fcount(file0)						# get the number of files
	#print("Found {0} files!\n".format(Image_No))	# display the number of images at that path
	return Image_No

def getWidth(name):
	# Get image pixel size (width x height)
	with Image.open(name) as img:
		width, height = img.size
	if width >= 900:
		print("{0} -> {1}".format(name, width))
	return width

def resize(name, cnt):
	basewidth = 600									# define new size
	img = Image.open(name)							# open image file
	wpercent = (basewidth / float(img.size[0]))
	hsize = int((float(img.size[1]) * float(wpercent)))
	img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
	img.save('resized_{}.jpg'.format(cnt))			# save the resized image

def main():
	images = No_images()
	print("Found {} files!\n".format(images))		# display the number of images at that path
	
	for cnt in range(0, images):					# Loop to each image file
		# Append the path and filename together
		name = ("{0}{1}".format(file0, os.listdir(file0)[cnt]))
		imagePath = name
		sizeW = getWidth(name)						# get the width of image
		if sizeW >= 900:							# if above 600 width
			resize(name, cnt)						# resize each image
	
	shutil.move(file1, dest)						# move to new folder

if __name__ == "__main__": main()
	
