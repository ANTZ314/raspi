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
#import btnClass as btn
import ledClass as leds
import oledClass as oled
import RPi.GPIO as GPIO

# BCM0 not working -> use BCM5, BCM6, BCM13
P_BTN1  = 0									# Push Button   (NC - Low)
P_BTN2  = 5									# Push Button   (NC - Low)
SWITCH	= 6									# Toggle Switch (NO - Low)

GPIO.setmode(GPIO.BCM)						# 
GPIO.setup(P_BTN1, GPIO.IN)					# External pull down
GPIO.setup(P_BTN2, GPIO.IN)					# External pull down
GPIO.setup(SWITCH, GPIO.IN)					# External pull up

###################
## MAIN FUNCTION ##
###################
def main():
	LEDS = leds.LEDClass()					# LED control class 
	#OLED = oled.OLEDClass()				# Instantiate OLED Class
	#BTN  = btn.btnClass()					# Instantiate Btn Class
		
	
	print "LET'S BEGIN!!"
	LEDS.All_Off1()							# LED 1 Off
	LEDS.All_Off2()							# LED 2 Off
	print "Start-up Mode:"
	
	GPIO.setmode(GPIO.BCM)					# type of GPIO
	GPIO.setup(P_BTN1, GPIO.IN)				# External pull down
	
	# Any main exceptions:
	try:
		try:
			while True:
				switch = GPIO.input(SWITCH)
				pb1 = GPIO.input(P_BTN1)
				pb2 = GPIO.input(P_BTN2)
				
				if switch == 0:
					LEDS.Blink_Purple1()
					print "Here1"
				elif pb1 == 1:
					LEDS.Blink_Cyan1()
					print "Here2"
				elif pb2 == 1:
					LEDS.Blink_Yellow1()
					print "Here3"
				#else:		
					#LEDS.Blink_Green1()
					#print "Here4"
						
						
		# Ctrl+C will exit the program correctly:
		except KeyboardInterrupt:
			print("\r\nEXIT PROGRAM!!")									# Pistol whip Thomas Wayne
			GPIO.cleanup()												# Kill Batmans parents
			sys.exit(0)
	
	# Any main exceptions save to log.txt file:
	except Exception:
		print("Exceptoin reached???")
		GPIO.cleanup()
		sys.exit(0)
		
if __name__ == "__main__":	main()
