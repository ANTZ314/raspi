# -*- coding: utf-8 -*-
"""
Description:
All LED controls, including all off, all on & 6 colors
"""
import RPi.GPIO as GPIO
import sys, time


class btnClass:
	P_BTN1  = 10							# Push Button   (NC - Low)
	P_BTN2  = 9								# Push Button   (NC - Low)
	SWITCH	= 11							# Toggle Switch (NO - Low)

	GPIO.setup(P_BTN1, GPIO.IN)				# External pull down
	GPIO.setup(P_BTN2, GPIO.IN)				# External pull down
	GPIO.setup(SWITCH, GPIO.IN)				# External pull up
	
	def __init__(self, **kwargs):
		print("BTN Class Init!!")
		
	###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~###
	def Btn1(self):
		btn1    = 0
		P_BTN1  = 10									# Push Button   (NC - Low)
		GPIO.setmode(GPIO.BCM)							# type of GPIO
		GPIO.setup(P_BTN1, GPIO.IN)						# External pull down
		btn1 = GPIO.input(P_BTN1)
		return btn1

	def Btn2(self):
		btn2    = 0
		P_BTN2  = 9										# Push Button   (NC - Low)
		GPIO.setmode(GPIO.BCM)							# type of GPIO
		GPIO.setup(P_BTN2, GPIO.IN)						# External pull down
		btn2 = GPIO.input(P_BTN2)
		return btn2
		
	def switch(self):
		switch1 = 0
		SWITCH  = 11									# Push Button   (NC - Low)
		GPIO.setmode(GPIO.BCM)							# type of GPIO
		GPIO.setup(SWITCH, GPIO.IN)						# External pull down
		switch1 = GPIO.input(SWITCH)
		return switch1
