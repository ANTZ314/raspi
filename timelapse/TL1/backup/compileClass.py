# -*- coding: utf-8 -*-
"""
Description:
Calls the bash file to convert multiple images into MP4 file
If file there, moves MP4 file to videos?
"""
import subprocess
import sys, os

#path1 = "/home/pi/Pictures/t_lapse/"					# path to timelapse directory
#path2 = "/home/pi/Videos/"								# patrh to compiled video directory

class compClass:
	def __init__(self, **kwargs):
		print("Compile Class Init!!")					# initialisation message
	
	def compile1(self):
		try:
			subprocess.call("./compile.sh")				# run bash file
			#raw_input("press Enter")					# wait here (if run in background?)
		except:
			print("Error")
					
	if __name__ == "__main__": main()


