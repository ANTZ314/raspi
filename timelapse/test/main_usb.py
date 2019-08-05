# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Test individual classes
"""
#import ledClass as leds
#import RPi.GPIO as GPIO
import usbClass as usb
import sys, time
#import picamera

## RASPI VERSION ##
#path1 = "/media/pi/"											# Destination Media path on USB
#path2 = "/home/pi/Pictures/4.jpg"								# Source path for converting/converted mp4 file
#path3 = "/home/pi/Pictures/lapse/frame%03d.jpg"				# Destination path for time lapse images
## UBUNTU VERSION ##
path1 = "/home/antz/Pictures/4.jpg"								# Source path for converting/converted mp4 file
path2 = "/media/antz/"											# Destination Media path on USB
path3 = "/home/antz/Pictures/lapse/frame%03d.jpg"				# Destination path for time lapse images

############################
## RasPi GPIO stuff here! ##
############################

#########################
## TIMELAPSE CAPTURING ##
#########################

#########################################
## VARIABLE PAUSE BTWN CAPTURED FRAMES ##
#########################################
## NOTE, GOES WITH:
##pause = raw_input("Pause 1 - 5: ")				# get number of secs from user
##check = pause.isdigit()							# check if entered value is a digit
def capture_wait(check, pause):			
	if check == True:
		for x in range (int(pause)):
			time.sleep(1)		
	else:
		print("Incorrect value!")

#################
# MAIN FUNCTION #
#################
def main():
	#LEDS = leds.LEDClass()							# create class instance
	USB = usb.usbClass()							# create class instance
	
	frame = 0										# initialise image name counter
	once1 = 0										# Capture Mode
	cap_flg = 0										# Capture flag
	print "LET'S BEGIN!!"
	#LEDS.All_Off1()								# LED 1 Off
	#LEDS.All_Off2()								# LED 2 Off
	print "Start-up Mode:"
	
	try:
		while True:
			# test LED blink functions #
			pause = raw_input("Pause 1 - 5: ")		# get value from user
			check = pause.isdigit()					# check if value is a digit
			capture_wait(check, pause)				# pause for that long
			USB.usb_put(path2)
			print("SUCCESS!")
			sys.exit(0)								# Take Martha's pearls
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")					# Pistol whip Thomas Wayne
		#GPIO.cleanup()								# Kill Batmans parents
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":	main()
