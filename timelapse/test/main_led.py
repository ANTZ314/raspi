# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Test individual classes
"""
import ledClass as leds
import RPi.GPIO as GPIO
import sys, time

#################
## GPIO INPUTS ##
#################

P_BTN1  = 10	# Push Button   (NC - Low)
P_BTN2  = 9		# Push Button   (NC - Low)
SWITCH	= 11	# Toggle Switch (NO - Low)

GPIO.setup(P_BTN1, GPIO.IN)		# External pull down
GPIO.setup(P_BTN2, GPIO.IN)		# External pull down
GPIO.setup(SWITCH, GPIO.IN)		# External pull up
	
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
	LEDS = leds.LEDClass()							# create class instance
	#USB = usb.usbClass()							# create class instance
	
	frame = 0										# initialise image name counter
	once1 = 0										# Capture Mode
	cap_flg = 0										# Capture flag
	print "LET'S BEGIN!!"
	LEDS.All_Off1()									# LED 1 Off
	LEDS.All_Off2()									# LED 2 Off
	print "Start-up Mode:"
	
	try:
		while True:
			raw_input("...")
			print "blue 1"
			LEDS.Blink_Blue1()
			raw_input("...")
			print "red 1"
			LEDS.Blink_Red1()
			raw_input("...")
			print "green 1"
			LEDS.Blink_Green1()
			raw_input("...")
			print "blue red 1"
			LEDS.Blink_BR1()
			raw_input("...")
			print "green blue 1"
			LEDS.Blink_GB1()
			raw_input("...")
			print "green red 1"
			LEDS.Blink_GR1()
			raw_input("...")
			print "blue 2"
			LEDS.Blink_Blue2()
			raw_input("...")
			print "red 2"
			LEDS.Blink_Red2()
			raw_input("...")
			print "green 2"
			LEDS.Blink_Green2()
			raw_input("...")
			print "blue red 2"
			LEDS.Blink_BR2()
			raw_input("...")
			print "green blue 2"
			LEDS.Blink_GB2()
			raw_input("...")
			print "green red 2"
			LEDS.Blink_GR2()
			raw_input("...")
			print "ALL 1"
			LEDS.Blink_All1()
			raw_input("...")
			print "ALL 2"
			LEDS.Blink_All2()
			raw_input("...")
			print("SUCCESS!")
			GPIO.cleanup()							# Kill Batmans parents
			sys.exit(0)								# Take Martha's pearls
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")					# Pistol whip Thomas Wayne
		GPIO.cleanup()								# Kill Batmans parents
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":	main()
