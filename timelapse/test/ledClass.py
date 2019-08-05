# -*- coding: utf-8 -*-
"""
Description:
All LED controls, including all off, all on & 6 colors
"""
import RPi.GPIO as GPIO
import sys, os, time


class LEDClass:
	# Define Pins (Using GPIO not header numbers)
	GREEN1 	= 2		# RGB - Green
	RED1	= 3		# RGB - Blue
	BLUE1 	= 4		# RGB - Red
	GREEN2 	= 17	# RGB - Green
	RED2  	= 27	# RGB - Blue
	BLUE2	= 22	# RGB - Red

	# Use BMC GPIO Numbers:
	GPIO.setmode(GPIO.BCM)

	# Pin Setup:
	print "Initialise Pins!"
	GPIO.setup(GREEN1, GPIO.OUT)	# set as output
	GPIO.setup(BLUE1, GPIO.OUT)		# set as output
	GPIO.setup(RED1, GPIO.OUT)		# set as output
	GPIO.setup(GREEN2, GPIO.OUT)	# set as output
	GPIO.setup(BLUE2, GPIO.OUT)		# set as output
	GPIO.setup(RED2, GPIO.OUT)		# set as output
	
	def __init__(self, **kwargs):
		print("Class init!!")
		
	###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~###
	def All_Off1(self):
		GPIO.output(self.GREEN1, GPIO.LOW)	# Green Off
		GPIO.output(self.BLUE1,  GPIO.LOW)	# Blue Off
		GPIO.output(self.RED1,   GPIO.LOW)	# Red Off
		
	def Blink_All1(self):
		GPIO.output(self.GREEN1, GPIO.HIGH)	# Green Off
		GPIO.output(self.BLUE1,  GPIO.HIGH)	# Blue Off
		GPIO.output(self.RED1,   GPIO.HIGH)	# Red Off
		time.sleep(0.5)
		GPIO.output(self.GREEN1, GPIO.LOW)	# Green Off
		GPIO.output(self.BLUE1,  GPIO.LOW)	# Blue Off
		GPIO.output(self.RED1,   GPIO.LOW)	# Red Off
		time.sleep(0.5)
		
	def Blink_Blue1(self):
		self.All_Off1()						# All Off
		self.All_Off2()						# All Off		
		GPIO.output(self.BLUE1,  GPIO.HIGH)	# Blue On
		time.sleep(0.5)
		GPIO.output(self.BLUE1,  GPIO.LOW)	# Blue Off
		time.sleep(0.5)

	def Blink_Red1(self):
		self.All_Off1()						# All Off
		self.All_Off2()						# All Off
		GPIO.output(self.RED1,   GPIO.HIGH)	# Red On
		time.sleep(0.5)
		GPIO.output(self.RED1,   GPIO.LOW)	# Red Off
		time.sleep(0.5)

	def Blink_Green1(self):
		self.All_Off1()						# All Off
		self.All_Off2()						# All Off
		GPIO.output(self.GREEN1, GPIO.HIGH)	# Green On
		time.sleep(0.5)
		GPIO.output(self.GREEN1, GPIO.LOW)	# Green Off
		time.sleep(0.5)

	def Blink_BR1(self):
		self.All_Off1()						# All Off
		self.All_Off2()						# All Off
		GPIO.output(self.BLUE1,  GPIO.HIGH)	# Blue On
		GPIO.output(self.RED1,   GPIO.HIGH)	# Red On
		time.sleep(0.5)
		GPIO.output(self.BLUE1,  GPIO.LOW)	# Blue Off
		GPIO.output(self.RED1,   GPIO.LOW)	# Red Off
		time.sleep(0.5)

	def Blink_GB1(self):
		self.All_Off1()						# All Off
		self.All_Off2()						# All Off
		GPIO.output(self.GREEN1, GPIO.HIGH)	# Green On
		GPIO.output(self.BLUE1,  GPIO.HIGH)	# Blue On
		time.sleep(0.5)
		GPIO.output(self.GREEN1, GPIO.LOW)	# Green Off
		GPIO.output(self.BLUE1,  GPIO.LOW)	# Blue On
		time.sleep(0.5)
		
	def Blink_GR1(self):
		self.All_Off1()						# All Off
		self.All_Off2()						# All Off
		GPIO.output(self.GREEN1, GPIO.HIGH)	# Green On
		GPIO.output(self.RED1,   GPIO.HIGH)	# Red Off
		time.sleep(0.5)
		GPIO.output(self.GREEN1, GPIO.LOW)	# Green Off
		GPIO.output(self.RED1,   GPIO.LOW)	# Red Off
		time.sleep(0.5)

	###~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LED 2 ~~~~~~~~~~~~~~~~~~~~~~~~~~###
	def All_Off2(self):
		GPIO.output(self.GREEN2, GPIO.LOW)	# Green Off
		GPIO.output(self.BLUE2,  GPIO.LOW)	# Blue Off
		GPIO.output(self.RED2,   GPIO.LOW)	# Red Off
		
	def Blink_All2(self):
		GPIO.output(self.GREEN2, GPIO.HIGH)	# Green Off
		GPIO.output(self.BLUE2,  GPIO.HIGH)	# Blue Off
		GPIO.output(self.RED2,   GPIO.HIGH)	# Red Off
		time.sleep(0.5)
		GPIO.output(self.GREEN2, GPIO.LOW)	# Green Off
		GPIO.output(self.BLUE2,  GPIO.LOW)	# Blue Off
		GPIO.output(self.RED2,   GPIO.LOW)	# Red Off
		time.sleep(0.5)
	
	def Blink_Blue2(self):
		self.All_Off1()						# All Off	
		self.All_Off2()						# All Off
		GPIO.output(self.BLUE2,  GPIO.HIGH)	# Blue On
		time.sleep(0.5)
		GPIO.output(self.BLUE2,  GPIO.LOW)	# Blue Off
		time.sleep(0.5)

	def Blink_Red2(self):
		self.All_Off1()						# All Off	
		self.All_Off2()						# All Off
		GPIO.output(self.RED2,   GPIO.HIGH)	# Red On
		time.sleep(0.5)
		GPIO.output(self.RED2,   GPIO.LOW)	# Red Off
		time.sleep(0.5)

	def Blink_Green2(self):
		self.All_Off1()						# All Off	
		self.All_Off2()						# All Off
		GPIO.output(self.GREEN2, GPIO.HIGH)	# Green On
		time.sleep(0.5)
		GPIO.output(self.GREEN2, GPIO.LOW)	# Green Off
		time.sleep(0.5)

	def Blink_BR2(self):
		self.All_Off1()						# All Off		
		GPIO.output(self.BLUE2,  GPIO.HIGH)	# Blue On
		GPIO.output(self.RED2,   GPIO.HIGH)	# Red On
		time.sleep(0.5)
		GPIO.output(self.BLUE2,  GPIO.LOW)	# Blue Off
		GPIO.output(self.RED2,   GPIO.LOW)	# Red Off
		time.sleep(0.5)

	def Blink_GB2(self):
		self.All_Off1()						# All Off	
		self.All_Off2()						# All Off
		GPIO.output(self.GREEN2, GPIO.HIGH)	# Green On
		GPIO.output(self.BLUE2,  GPIO.HIGH)	# Blue On
		time.sleep(0.5)
		GPIO.output(self.GREEN2, GPIO.LOW)	# Green Off
		GPIO.output(self.BLUE2,  GPIO.LOW)	# Blue On
		time.sleep(0.5)
		
	def Blink_GR2(self):
		self.All_Off1()						# All Off	
		self.All_Off2()						# All Off
		GPIO.output(self.GREEN2, GPIO.HIGH)	# Green On
		GPIO.output(self.RED2,   GPIO.HIGH)	# Red Off
		time.sleep(0.5)
		GPIO.output(self.GREEN2, GPIO.LOW)	# Green Off
		GPIO.output(self.RED2,   GPIO.LOW)	# Red Off
		time.sleep(0.5)
		
