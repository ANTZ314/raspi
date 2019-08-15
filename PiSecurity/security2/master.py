#!/usr/bin/env python
"""
Created:		A.Smith [2017-08]
Description:	Run shell script for main security python code
				Trying to avoid picamera resourse error
				chmod +x master.sh
"""
import sys, os, time
import subprocess
import traceback
#import ledClass as leds
import RPi.GPIO as GPIO

###################
## MAIN FUNCTION ##
###################
def main():		
	try:
		try:	
			#os.chdir("/home/pi/test")
			#subprocess.call("./master.sh", shell=True)
			os.chdir("/home/pi/security")
			subprocess.call("python main.py --conf conf.json", shell=True)
			#sys.exit(0)
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("master.py - keyboard interupt")
			#GPIO.cleanup()
			sys.exit(0)
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("master.py - Exceptoin reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		GPIO.cleanup()
		sys.exit(0)

if __name__ == "__main__":	main()
