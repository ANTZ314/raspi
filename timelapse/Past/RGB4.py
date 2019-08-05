# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Testing button toggling
"""
import RPi.GPIO as GPIO
import sys, time

# Define Pins
ledPin1 = 23	# Blue
btnPin  = 25	# Button
# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Pin Setup:
print "Initialise Pins!"
GPIO.setup(ledPin1, GPIO.OUT)	# set as output
GPIO.setup(btnPin, GPIO.IN)		# already have pull down

def main():
	flag1 = 0
	print "Start loop!"
	GPIO.output(ledPin1, GPIO.HIGH)

	try:
		while True:			
			if GPIO.input(btnPin) == 0:		# if btn LOW
				flag1 = not flag1
			
			if flag1:
				GPIO.output(ledPin1, GPIO.HIGH)
				time.sleep(1)
				GPIO.output(ledPin1, GPIO.LOW)
				time.sleep(1)
			else:							#
				GPIO.output(ledPin1, GPIO.HIGH)
				time.sleep(0.2)
				GPIO.output(ledPin1, GPIO.LOW)
				time.sleep(0.2)
	
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		GPIO.cleanup()		# cleanup after the crime
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
