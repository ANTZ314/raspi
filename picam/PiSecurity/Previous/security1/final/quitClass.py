# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Automatically shutdown the RasPi using Shell Script
"""
import sys
import subprocess
import RPi.GPIO as GPIO

class quitClass:
	def __init__(self, **kwargs):
		print("Quit Class init!!")

	def quit1(self):
		try:
			print("Shutting Down!!")
			GPIO.cleanup()							# cleanup after the crime
			subprocess.call("./shutdown.sh")			# run Terminal shutdown command sequence
			sys.exit(0)									# Can exit python before Bash
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			GPIO.cleanup()								# cleanup after the crime
			print("\r\nEXIT PROGRAM!!")
			sys.exit(0)
