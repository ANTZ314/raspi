# -*- coding: utf-8 -*-
"""
Description:
All LED controls, including all off, all on & 6 colors
"""
import RPi.GPIO as GPIO
import sys, time


class LEDClass:
	# Define Pins (Using GPIO not header numbers)
	GREEN1 	= 3						# RGB - Green
	RED1	= 2						# RGB - Red
	#BTN 	= 4						# Button

	# Use BMC GPIO Numbers:
	GPIO.setmode(GPIO.BCM)			# type of GPIO

	# Pin Setup:
	GPIO.setup(GREEN1, GPIO.OUT)	# set as output
	GPIO.setup(RED1, GPIO.OUT)		# set as output
	#GPIO.setup(BTN, GPIO.IN)		# set as input
	
	def __init__(self, **kwargs):
		print("LED Class Init!!")
		
	###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~###
	def Blink_Red1(self):
		GPIO.output(self.GREEN1,  GPIO.HIGH)		# Green Off
		
		GPIO.output(self.RED1,   GPIO.LOW)		# Red On
		time.sleep(0.5)	
		GPIO.output(self.RED1,   GPIO.HIGH)		# Red Off
		time.sleep(0.5)

	def Blink_Green1(self):
		GPIO.output(self.RED1,  GPIO.HIGH)		# Red Off
		
		GPIO.output(self.GREEN1, GPIO.LOW)		# Green On
		time.sleep(0.5)
		GPIO.output(self.GREEN1, GPIO.HIGH)		# Green Off
		time.sleep(0.5)

	def Quick_Red1(self):
		GPIO.output(self.GREEN1,  GPIO.HIGH)		# Green Off
				
		GPIO.output(self.RED1,  GPIO.LOW)		# Red On
		time.sleep(0.1)
		GPIO.output(self.RED1,  GPIO.HIGH)		# Red Off
		time.sleep(0.1)

	def Quick_Green1(self):
		GPIO.output(self.RED1,  GPIO.HIGH)		# Red Off
			
		GPIO.output(self.GREEN1,  GPIO.LOW)	# Green On
		time.sleep(0.1)
		GPIO.output(self.GREEN1,  GPIO.HIGH)		# Green Off
		time.sleep(0.1)
		
