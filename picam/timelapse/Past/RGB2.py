# -*- coding: utf-8 -*-
"""
Description:
	BLinks RGB LED for on second on each:
	 - GPIO_18 = GREEN
	 - GPIO_23 = BLUE
	 - GPIO_24 = RED
"""

import RPi.GPIO as GPIO
import sys, time
 
# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Set GPIO18/23/24 as an output
print "Setup Pin 18/23/24"
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

def main():
	var=1
	print "Start loop!"
	GPIO.output(18, GPIO.HIGH)
	GPIO.output(23, GPIO.HIGH)
	GPIO.output(24, GPIO.HIGH)

	try:
		while True:
			print "ALL OFF"
			GPIO.output(18, GPIO.HIGH)
			GPIO.output(23, GPIO.HIGH)
			GPIO.output(24, GPIO.HIGH)
			time.sleep(1)
			
			print "RED"
			GPIO.output(18, GPIO.HIGH)
			GPIO.output(23, GPIO.HIGH)
			GPIO.output(24, GPIO.LOW)
			time.sleep(1)
			
			print "GREEN"
			GPIO.output(18, GPIO.LOW)
			GPIO.output(23, GPIO.HIGH)
			GPIO.output(24, GPIO.HIGH)
			time.sleep(1)
			
			print "BLUE"
			GPIO.output(18, GPIO.HIGH)
			GPIO.output(23, GPIO.LOW)
			GPIO.output(24, GPIO.HIGH)
			time.sleep(1)
			
			print "ALL ON"
			GPIO.output(18, GPIO.LOW)
			GPIO.output(23, GPIO.LOW)
			GPIO.output(24, GPIO.LOW)
			time.sleep(1)
			
	except KeyboardInterrupt:
		GPIO.cleanup()
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
