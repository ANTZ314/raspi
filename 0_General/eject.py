# -*- coding: utf-8 -*-
"""
Description:
	properly eject USB for re-insertion later
	List usb drives: lsblk
	
Requirement:
	sudo apt install eject
"""
import os
#import sys, time
import traceback
#import subprocess


###################
## MAIN FUNCTION ##
###################
def main():
	#cmd = "sudo umount /dev/sda1"
	cmd = "sudo umount /media/pi/*"
	
	try:
		try:
			print("Eject USB")
			os.system(cmd)
			print("Done?")
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("keyboard interrupt")
			sys.exit(0)
	
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("Exception Reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		sys.exit(0)

if __name__ == "__main__":	main()
