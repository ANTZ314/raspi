# -*- coding: utf-8 -*-
"""
Description: If .jpg, get each filename
			 Resize each file according to new length
			 [800xsize] for the 7" LCD
			 Save each resized image into new folder 
			 increment each new filename
"""

import PIL
from PIL import Image
import sys
import os

file0 = 'img1.jpg'
file1 = 'img2.jpg'

""" Counts the number of files in a directory """
def fcount1(path):
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1

    return count

def main():
	cnt = 0															# new file counter
	file_path1 = "/home/antz/0_Python/image/Armadillo/pics"			# path to woring directory
	file_path2 = "/home/antz/0_Python/image/Armadillo/new"			# path for new images
	
	## Check for directory, if not then create it ##
	directory = os.path.dirname(file_path1)								# check in images file path
	if not os.path.exists(directory):									# if directory doesn't exist
		print("File path doesn't exist!")								# Notify that directory was created
		#os.makedirs(directory)											# Create the directory
	else:
		files = fcount1(file_path1)
		print(str(file_path1) + " has " + str(files) + " files!")		# print the file path
		try:															# 
			# print the name of each file in the given folder
			for file in os.listdir(file_path1):							# each file in that folder
				if file.endswith(".jpg"):								# only do if .jpg file
					pics = os.path.join(file_path1, file)
					cnt += 1
					name = "img{}.jpg".format(str(cnt))						# create new name
					new = os.path.join(file_path2, name)				# append file path
					
					# Resize each image to screen length x %width
					basewidth = 800
					hsize = 480
					img = Image.open(pics)
					wpercent = (basewidth / float(img.size[0]))
					hsize = int((float(img.size[1]) * float(wpercent)))
					img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
					#print(new)
					img.save(new)										# save in new folder
		except:
			print("Exception Ocurred...")
	print("COMPLETE!!")
	sys.exit()
	

if __name__ == "__main__": main()
