# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	Continuously switch between software PWM duty Cycle
				20% <-> 80%
"""
import RPi.GPIO as GPIO
import sys, time

# Define Pins
pwmPin  = 18	# Green
ledPin1 = 23	# Blue
ledPin2 = 24	# Red
btnPin  = 25	# Button
DC		= 80	# Duty Cycle (0-100)
# Use BMC GPIO Numbers:
GPIO.setmode(GPIO.BCM)

# Pin Setup:
print "Initialise Pins!"
GPIO.setup(pwmPin, GPIO.OUT)	# set as output
pwm = GPIO.PWM(pwmPin, 50)		# Init PWM to 100Hz freq
GPIO.setup(ledPin1, GPIO.OUT)	# set as output
GPIO.setup(ledPin2, GPIO.OUT)	# set as output
#GPIO.setup(btnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)	# internal
GPIO.setup(btnPin, GPIO.IN)		# already have pull down

def main():
	
	print "Start loop!"
	GPIO.output(23, GPIO.HIGH)
	GPIO.output(24, GPIO.HIGH)
	#GPIO.output(18, GPIO.HIGH)
	pwm.start(50)

	try:
		while True:			
			if GPIO.input(btnPin):		# if btn LOW
				print "80% GREEN"
				pwm.ChangeDutyCycle(100-DC)	# 20%
				time.sleep(1)
			
			else:							# if btn HIGH
				print "20% GREEN"
				pwm.ChangeDutyCycle(DC)		# 80%
				time.sleep(1)
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		pwm.stop()			# kill Batmans parents
		GPIO.cleanup()		# cleanup after the crime
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
