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
	path1 = "/home/pi/Videos/4.jpg"									# RasPi - path to timelapse directory
	path2 = "/media/pi/"											# RasPi - path to media
	path3 = "/home/pi/Pictures/t_lapse/"							# Image source directory
	
	## PC ##
	#path1 = "/home/antz/Videos/4.jpg"								# PC - path to timelapse directory
	#path2 = "/media/antz/"											# PC - path to media
	#path3 = "/home/antz/Pictures/t_lapse/"							# Image source directory

	def __init__(self, **kwargs):
		print("USB Class initialised!")

	def usb_put(self, path2):
		try:
			path2 = glob(path2 + "*/")								# returns as list item
			print(path2[0])											# must ref item[0]
				
			## Check for USB destination path ##
			directory = os.path.dirname(path2[0])					# check in images file path
			if not os.path.exists(directory):						# if directory doesn't exist
				print("Directory doesn't exist!")					# Notify if directory was created
			else:
				print("path exists")
				try:												# [Skip if file doesn't exist]
					## Copy file to new destination ##
					src = self.path1
					dst = path2[0]
					## move the file to destination folder ##
					shutil.move(src, dst)
					print("Copied to USB!")
					## Empty source folder ##
					print("Clear Images")
					shutil.rmtree(self.path3)						# remove folder and contents
					os.makedirs(self.path3)							# create new folder of same name
				except:
					print("USB Routine Error...")					# Notify user
					sys.exit(0)										# exit properly 
		except:
			print("Main USB Error")									# usually no USB Device
