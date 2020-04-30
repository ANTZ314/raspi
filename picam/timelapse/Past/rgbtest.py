# -*- coding: utf-8 -*-
"""
Description:
	BLinks RGB LED for on second on each:
	 - GPIO_ = GREEN
	 - GPIO_ = BLUE
	 - GPIO_ = RED
	 - GPIO_ = GREEN
	 - GPIO_ = BLUE
	 - GPIO_ = RED
"""

import RPi.GPIO as GPIO
import sys, time
 
# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Set GPIO18/23/24 as an output
print "Setup Pin 18/23/24"
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

def main():
	var=1
	print "Start loop!"
	GPIO.output(2, GPIO.LOW)
	GPIO.output(3, GPIO.LOW)
	GPIO.output(4, GPIO.LOW)
	GPIO.output(17, GPIO.LOW)
	GPIO.output(27, GPIO.LOW)
	GPIO.output(22, GPIO.LOW)

	try:
		while True:
			print "ALL ON"
			GPIO.output(2, GPIO.HIGH)
			GPIO.output(3, GPIO.HIGH)
			GPIO.output(4, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(17, GPIO.HIGH)
			GPIO.output(27, GPIO.HIGH)
			GPIO.output(22, GPIO.HIGH)
			time.sleep(1)
			
			print "RED"
			GPIO.output(2, GPIO.LOW)
			GPIO.output(3, GPIO.HIGH)
			GPIO.output(4, GPIO.LOW)
			time.sleep(1)
			GPIO.output(17, GPIO.LOW)
			GPIO.output(27, GPIO.HIGH)
			GPIO.output(22, GPIO.LOW)
			time.sleep(1)
			
			print "GREEN"
			GPIO.output(2, GPIO.HIGH)
			GPIO.output(3, GPIO.LOW)
			GPIO.output(4, GPIO.LOW)
			time.sleep(1)
			GPIO.output(17, GPIO.HIGH)
			GPIO.output(27, GPIO.LOW)
			GPIO.output(22, GPIO.LOW)
			time.sleep(1)
			
			print "BLUE"
			GPIO.output(2, GPIO.LOW)
			GPIO.output(3, GPIO.LOW)
			GPIO.output(4, GPIO.HIGH)
			time.sleep(1)
			GPIO.output(17, GPIO.LOW)
			GPIO.output(27, GPIO.LOW)
			GPIO.output(22, GPIO.HIGH)
			time.sleep(1)
			
			print "ALL OFF"
			GPIO.output(2, GPIO.LOW)
			GPIO.output(3, GPIO.LOW)
			GPIO.output(4, GPIO.LOW)
			time.sleep(1)
			GPIO.output(17, GPIO.LOW)
			GPIO.output(27, GPIO.LOW)
			GPIO.output(22, GPIO.LOW)
			time.sleep(1)
			
	except KeyboardInterrupt:
		print "ALL OFF"
		GPIO.output(2, GPIO.LOW)
		GPIO.output(3, GPIO.LOW)
		GPIO.output(4, GPIO.LOW)
		GPIO.output(17, GPIO.LOW)
		GPIO.output(27, GPIO.LOW)
		GPIO.output(22, GPIO.LOW)
		GPIO.cleanup()
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
