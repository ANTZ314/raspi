# -*- coding: utf-8 -*-
"""
Description:
All LED controls, including all off, all on & 6 colors
"""
import sys, time
import RPi.GPIO as GPIO

class miniClass:
	def __init__(self, **kwargs):
		print("LED Class Init!!")
		
	###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~###
	def Quick_Red2(self):
		RED3  	= 27					# RGB - Red
		GPIO.setmode(GPIO.BCM)			# type of GPIO
		GPIO.setup(RED3, GPIO.OUT)		# set as output
		# Blink Red
		GPIO.output(RED3,  GPIO.HIGH)	# Red On
		time.sleep(0.1)
		GPIO.output(RED3,  GPIO.LOW)	# Red Off
		time.sleep(0.1)
		GPIO.output(RED3,  GPIO.HIGH)	# Red On
		time.sleep(0.1)
		GPIO.output(RED3,  GPIO.LOW)	# Red Off
		time.sleep(0.1)

	def Btn1(self):
		btn1    = 0
		P_BTN1  = 10										# Push Button   (NC - Low)
		GPIO.setmode(GPIO.BCM)								# type of GPIO
		GPIO.setup(P_BTN1, GPIO.IN)							# External pull down
		btn1 = GPIO.input(P_BTN1)
		return btn1

	def Btn2(self):
		btn2    = 0
		P_BTN2  = 9											# Push Button   (NC - Low)
		GPIO.setmode(GPIO.BCM)								# type of GPIO
		GPIO.setup(P_BTN2, GPIO.IN)							# External pull down
		btn2 = GPIO.input(P_BTN2)
		return btn2
