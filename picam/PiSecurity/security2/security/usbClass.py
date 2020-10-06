# -*- coding: utf-8 -*-
"""
Description:
Checks for USB device, if found,
Moves the specified file to the new specified path
"""

import sys, os, shutil
from glob import glob

class usbClass:
	## RASPI ##
	path1 = "/media/pi/"												# Path to media directory
	#path1 = "/media/root/"												# Path changed ? ? ?
	path2 = "/home/pi/Pictures/security/"								# Path to images source directory
	path3 = "/home/pi/Pictures/security"								# New image source directory

	def __init__(self, **kwargs):
		print("USB Class Init!!")

	def usb_put(self, path1, path2):									# destination folder (USB)
		try:
			path1 = glob(path1 + "*/")									# returns as list item
			## Check for USB destination path ##
			directory = os.path.dirname(path1[0])						# check in images file path
			
			if not os.path.exists(directory):							# if directory doesn't exist
				print("Directory doesn't exist!")						# Notify if directory was created
			else:
				print("path exists")
				try:													# [Skip if file doesn't exist]
					## Copy file to new destination ##
					src = self.path2									# images folder
					dst = path1[0]										# USB
					#print(self.path2)									# display the path
					print("Source: " + src)
					print("Destination: " + dst)
					## move the file to destination folder ##
					print("here")
					shutil.move(src, dst)
					print("Copied to USB!")
					## Empty source folder ##
					print("Clear Images")
					shutil.rmtree(self.path2, ignore_errors=True)		# remove folder and contents
					os.makedirs(self.path3)								# create new folder of same name
					return 1
				except:
					print("USB Routine Error...")						# Notify user
					#sys.exit(0)										# exit properly 
					return 0											# return Error code
		except:
			print("Main USB Error")										# usually no USB Device
			#sys.exit(0)	
			return 0													# return Error code
