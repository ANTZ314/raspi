#!/usr/bin/env python
"""
Created By:
	A.Smith [2017-08]

Description:	
	Open the appropriate folder an d run python script
	Avoids resource error found in running resources from boot
	Also includes error exceptions & logging
	Place this file in root folder

Run at boot:
	$ sudo crontab -e
	@reboot sleep 35 && sudo python /home/pi/boot_run.py &
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
			os.chdir("/home/pi/main")
			subprocess.call("python main.py", shell=True)
			#sys.exit(0)
			
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			print("master.py - keyboard interupt")
			GPIO.cleanup()
			sys.exit(0)
	# Any Main Errors saved to log.txt file:
	except Exception:
		print("master.py - Exceptoin reached")
		log = open("log.txt", 'w')
		traceback.print_exc(file=log)
		GPIO.cleanup()
		sys.exit(0)

if __name__ == "__main__":	main()
