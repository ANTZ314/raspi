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
	def __init__(self, **kwargs):
		print("Quit Class initialised!")

	def quit1(self):
		LED = mini.miniClass()							# create instance

		try:
			LED.Quick_Red2()							# warining
			while 1:
				if LED.Btn1() == 1:
					print("Go back!")
					break
					#raw_input("Are you sure?")
				if LED.Btn2() == 1:
					LED.Quick_Blue2()					# Execute
					#self.GPIO.cleanup()				# cleanup after the crime
					#subprocess.call("./shutdown.sh")	# run Terminal shutdown command sequence
					#sys.exit(0)						# Can exit python before Bash
				LED.Quick_Red2()
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			GPIO.cleanup()								# cleanup after the crime
			print("\r\nEXIT PROGRAM!!")
			sys.exit(0)
