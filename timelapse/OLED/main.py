# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	
"""
import OLEDtext as OLED
import RPi.GPIO as GPIO
import sys, time

OLED_RST = 18

# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Pin Setup:
print "Initialise Pins!"
GPIO.setup(OLED_RST, GPIO.OUT)		# set as output

#################
# MAIN FUNCTION #
#################
def main():	
	oled = OLED.OLEDtext()			# create class object
	
	print "LET'S BEGIN!!"
	
	try:
		oled.clear_oled()
		oled.draw(1)
		while True:
			#oled.draw(1)
			print("test1")
			time.sleep(2)
			print("test1")
			#oled.draw(2)
			time.sleep(2)			
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")
		GPIO.output(OLED_RST, GPIO.HIGH)
		time.sleep(1)
		GPIO.output(OLED_RST, GPIO.LOW)
		sys.exit(0)	

if __name__ == "__main__":
	main()
