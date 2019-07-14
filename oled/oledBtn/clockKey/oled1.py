#!/usr/bin/env python
"""
# -*- coding: utf-8 -*-
Description:
PyImageSearch Surveillance Example edited out DropBox storage

USAGE:
$ python security1.py --conf conf1.json
"""
# import the necessary packages
import gaugette.ssd1306
import gaugette.platform
import gaugette.gpio
import datetime
import time, sys, os
import oledClass as oled
import RPi.GPIO as GPIO

###################
## MAIN FUNCTION ##
###################
def main():
	OLED = oled.OLEDClass()
		
	print "HELLO!! LET'S BEGIN!!"
	
	# Any main exceptions:
	try:
		try:
			OLED.OLEDInitialise()
			
			while True:
				raw_input("press key to continue...")
				OLED.OLEDClock()
		# Ctrl+C will exit the program correctly:
		except KeyboardInterrupt:
			print("\r\nEXIT PROGRAM!!")									# Pistol whip Thomas Wayne
			#GPIO.cleanup()												# Kill Batmans parents
			sys.exit(0)
	
	# Any main exceptions save to log.txt file:
	except Exception:
		print("Exceptoin reached???")
		#GPIO.cleanup()
		sys.exit(0)
		
if __name__ == "__main__":	main()
