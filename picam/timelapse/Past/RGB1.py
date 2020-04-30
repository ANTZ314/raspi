# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	When button is Open, continuously switch between software 
				PWM duty Cycle (20% <-> 80%)
				When button is Closed Blink Red then  Blue continuously
"""
import RPi.GPIO as GPIO
import sys, time

# Define Pins
pwmPin  = 18	# Green
ledPin1 = 23	# Blue
ledPin2 = 24	# Red
btnPin  = 25	# Button
DC		= 20	# Duty Cycle (0-100)
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
	print "ALL OFF"
	GPIO.output(23, GPIO.HIGH)
	GPIO.output(24, GPIO.HIGH)
	#GPIO.output(18, GPIO.HIGH)
	pwm.start(50)

	try:
		while True:
			if GPIO.input(btnPin):			# if btn LOW
				print "RED"
				GPIO.output(18, GPIO.HIGH)
				GPIO.output(23, GPIO.HIGH)
				GPIO.output(24, GPIO.LOW)	# Red On
				time.sleep(1)
				
				print "BLUE"
				GPIO.output(18, GPIO.HIGH)
				GPIO.output(23, GPIO.LOW)	# Blue On
				GPIO.output(24, GPIO.HIGH)
				time.sleep(1)
			
			else:							# if btn HIGH
				print "95% GREEN"
				pwm.ChangeDutyCycle(DC)		# 95%
				GPIO.output(23, GPIO.HIGH)	# Red Off
				GPIO.output(24, GPIO.HIGH)	# Blue Off
				time.sleep(3)
				print "5% GREEN"
				pwm.ChangeDutyCycle(100-DC)	# 5%
				time.sleep(3)
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		pwm.stop()			# kill Batmans parents in a dark alley
		GPIO.cleanup()		# cleanup after the crime (take Martha's pearls)
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
