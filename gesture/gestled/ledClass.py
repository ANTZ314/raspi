# -*- coding: utf-8 -*-
"""
Description:
Blink single LED on pin 8 multiple times
"""
import RPi.GPIO as GPIO
import sys, time


class LEDClass:
	# Define Pins (Using GPIO not header numbers)
	#BLUE 	= 14				# GPIO14 = pin 8
	BLUE 	= 8					# pin 8 = GPIO 14

	# Use BMC GPIO Numbers:
	#GPIO.setmode(GPIO.BCM)		# GPIO numbers
	GPIO.setmode(GPIO.BOARD)	# actual pin numbers
	# Pin Setup:
	GPIO.setup(BLUE, GPIO.OUT)	# set as output
	
	def __init__(self, **kwargs):
		print("LED Class Init!!")
		
	###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~###
	def All_Off1(self):		
		BLUE 	= 14						# RGB - Green
		GPIO.output(self.BLUE,   GPIO.LOW)	# Red Off
		
	def Blink_1(self):
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)
		
	def Blink_2(self):
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)

	def Blink_3(self):
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)

	def Blink_4(self):
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.HIGH)	# Green Off
		time.sleep(0.2)
		GPIO.output(self.BLUE, GPIO.LOW)	# Green Off
		time.sleep(0.2)
