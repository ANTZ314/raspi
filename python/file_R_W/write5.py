# -*- coding: utf-8 -*-
"""
Python 2.7 (virtual env)
-> If file doesn't exist, file is created
-> If exists, opens existing file reads & prints contents
-> Appends the names of each file in the folder of "file_path2" 
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
	#file_path2 = "../image"								# Go one folder up then into images
	file_path1 = "/home/antz/0Python/files"					# path to woring director
	file_path2 = "/home/antz/0_CV3/pics"					# path to images
	exists = 0												# Append after printing contents
	FaceNum = 5												# Temporary predefined number of faces
	Image_No = 0

	#print("Found {0} faces!\n".format(FaceNum))			# display number of faces found (find later)
	
	## Check for directory, if not then create it ##
	directory = os.path.dirname(file_path2)					# check in images file path
	if not os.path.exists(directory):						# if directory doesn't exist
		os.makedirs(directory)								# Create the directory
		#print("Image Directory Created!")					# Notify if directory was created
	else:
		Image_No = fcount(file_path2)						# get the number of images in the folder
		#print("Image Directory Exists!")					# Notify if image directory exists
		try:												# [Skip if file doesn't exist]
			exists = 0										# Clear flag
			file = open('FaceCount.txt', 'r') 				# Open to read file
			print (file.read())								# Print the contents
			file.close()									# Close the file
		except:
			print("No file to read...")						# Notify user
			file= open("FaceCount.txt","a+")				# Append to file (will create file also)
			for cnt in range(0, Image_No):					# for each file in image folder
				file.write("{0}\r\n".format(os.listdir(file_path2)[cnt]))   # append the file name
				file.write("Number of faces: {0}\r\n".format(FaceNum)) 		# append the no. of faces
			file.write("=" * 18)							# mark last entry
			file.close()									# close the file
			exists = 1										# Don't append twice if file exists
			
		if exists == 0:										# Append after printing contents
			file= open("FaceCount.txt","a+")				# Append to file (no need to create file)
			for cnt in range(0, Image_No):					# for each file in image folder
				file.write("{0}\r\n".format(os.listdir(file_path2)[cnt]))   # append the file name
				file.write("Number of faces: {0}\r\n".format(FaceNum)) 		# append the no. of faces
			file.write("=" * 18)							# mark last entry
			file.close()									# close the file
			print "The File was appended..."
		else:												# Notify of file creation
			print "The File was created..."					# notification	
		
		
if __name__ == "__main__": main()
