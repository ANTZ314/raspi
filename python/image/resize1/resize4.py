# -*- coding: utf-8 -*-
"""
Description: gets the name and size of each .jpg file in the given folder
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
	file_path1 = "/home/antz/0_Python/image/Armadillo/pics"			# path to woring directory
	
	## Check for directory, if not then create it ##
	directory = os.path.dirname(file_path1)							# check in images file path
	if not os.path.exists(directory):								# if directory doesn't exist
		print("File path doesn't exist!")							# Notify that directory was created
		#os.makedirs(directory)										# Create the directory
	else:
		files = fcount1(file_path1)
		print(str(file_path1) + " has " + str(files) + " files!")	# print the file path
		try:														# 
			# print the name of each file in the given folder
			for file in os.listdir(file_path1):						# each file in that folder
				if file.endswith(".jpg"):							# only do if .jpg file
					pics = os.path.join(file_path1, file)
					# Get image pixel size (width x height)
					with Image.open(str(pics)) as img:
						width, height = img.size
					print('{0}: {1}x{2}'.format(pics, width, height))
		except:
			print("Exception Ocurred...")
	

if __name__ == "__main__": main()
