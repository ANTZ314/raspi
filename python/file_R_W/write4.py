# -*- coding: utf-8 -*-
"""
Python 2.7 (virtual env)
-> If image directory doesn't exist, directory is created
-> If 'FaceCount.txt' file doesn't exist, file is created
-> If exists, opens existing file & reads
-> Appends each file name in "file_path2" folder to .txt
"""

import sys
import os


def fcount(path):
    """ Counts the number of files in a directory """
    count = 0
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            count += 1

    return count

def main():
	exists = 0												# variable to append after printing contents
	cnt = 0													# generic counter
	#file_path1 = "/home/antz/0Python/files/notes.txt"		# path to note storage
	file_path1 = "/home/antz/0Python/files"					# path to working directory
	file_path2 = "/home/antz/0_CV3/pics"					# path to images
	exists = 0												# Append after printing contents
	FaceNum = 5
	Image_No = 0

	Image_No = fcount(file_path2)							# get the number of images in the folder
	print("Found {0} faces!".format(FaceNum))				# display number of faces found (find later)
	print("Found {0} files!\n".format(Image_No))			# display the number of images at that path
	
	for cnt in range(0, Image_No):							# loop number of images found
		try:												# Skip if file doesn't exist
			exists = 0										# Clear flag
			file = open('FaceCount.txt', 'r') 				# Open to read file
			#print file.read()								# Print the contents
			file.close()									# Close the file
		except:
			exists = 1										# Don't append twice if file exists
			file = open("FaceCount.txt","a+")				# Create/open file then Append data 
			file.write("Image Path: {0}\r\n".format(file_path2))
			file.write("Filename: {0}\r\n".format(os.listdir(file_path2)[cnt]))
			file.write("Number of faces: {0}\r\n\n".format(FaceNum))
			file.close()									# Exit the opened file

		if exists == 0:										# Append after printing contents
			file = open("FaceCount.txt","a+")				# Create/open file then Append data 
			file.write("Image Path: {0}\r\n".format(file_path2))
			file.write("Filename: {0}\r\n".format(os.listdir(file_path2)[cnt]))
			file.write("Number of faces: {0}\r\n\n".format(FaceNum))
			file.close()									# Exit the opened file
			print ("{0} was appended".format(os.listdir(file_path2)[cnt]))	# notification
		else:												# Notify of file creation
			print ("The File was created...")				# notification	
		
		
if __name__ == "__main__": main()
