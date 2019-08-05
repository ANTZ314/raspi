# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Testing button toggling
"""
import sys
import subprocess
import ledMini as mini
import RPi.GPIO as GPIO

class quitClass:
	GPIO.setmode(GPIO.BCM)						# type of GPIO
	
	def __init__(self, **kwargs):
		print("Quit Class initialised!")

	def quit1(self):
		LED = mini.miniClass()					# create instance

		try:
			LED.Quick_Red2()					# warining
			raw_input("Are you sure?")
			LED.Quick_Red2()					# Execute
			print("\r\nEXIT PROGRAM!!")			# Exit
			#self.GPIO.cleanup()						# cleanup after the crime
			#subprocess.call("./shutdown.sh")	# run Terminal shutdown command sequence
			sys.exit(0)							# Can exit python before Bash
		
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			GPIO.cleanup()						# cleanup after the crime
			print("\r\nEXIT PROGRAM!!")
			sys.exit(0)
