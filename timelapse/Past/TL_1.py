# -*- coding: utf-8 -*-
"""
Created:		A.Smith [2017-08]
Description:	When button is Open, continuously switch between software 
				PWM duty Cycle (20% <-> 80%)
				When button is Closed Blink Red then  Blue continuously
"""
import RPi.GPIO as GPIO
import sys, time
import picamera

# Define Pins
pwmPin  = 18	# Green
ledPin1 = 23	# Blue
ledPin2 = 24	# Red
btnPin  = 25	# Button
DC		= 10	# Duty Cycle (0-100)
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

def capture_frame(frame):
    with picamera.PiCamera() as cam:
        time.sleep(2)
        cam.capture('/home/pi/Pictures/lapse/frame%03d.jpg' % frame)

def main():
	frame = 0					# initialise image name counter
	print "LET'S BEGIN!!"
	GPIO.output(23, GPIO.HIGH)	# Blue Off
	GPIO.output(24, GPIO.HIGH)	# Red off
	# Start Green at 50% D.C.
	pwm.start(50)				# GPIO.output(18, GPIO.HIGH)
	print "Initial Mode:"
	
	try:
		while True:
			if GPIO.input(btnPin):			# if btn LOW
				# indicate capture
				GPIO.output(18, GPIO.HIGH)
				GPIO.output(23, GPIO.HIGH)
				GPIO.output(24, GPIO.LOW)	# Red On
				# Capture and image
				capture_frame(frame)
				#time.sleep(2)				# delay before next capture
				print "RED  - Image Captured!"				
				# Increment image name counter
				frame += 1
				
				# indicate next capture
				GPIO.output(18, GPIO.HIGH)
				GPIO.output(23, GPIO.LOW)	# Blue On
				GPIO.output(24, GPIO.HIGH)
				# Capture and image
				capture_frame(frame)
				#time.sleep(2)				# delay before next capture				
				print "BLUE - Image Captured!"				
				# Increment image name counter
				frame += 1
			
			else:							# if btn HIGH
				frame = 0					# Clear Frame Counter
				print "90% GREEN"
				pwm.ChangeDutyCycle(DC)		# 90%
				GPIO.output(23, GPIO.HIGH)	# Red Off
				GPIO.output(24, GPIO.HIGH)	# Blue Off
				time.sleep(2)
				print "10% GREEN"
				pwm.ChangeDutyCycle(100-DC)	# 10%
				time.sleep(2)
			
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		pwm.stop()			# kill Batmans parents in a dark alley
		GPIO.cleanup()		# cleanup after the crime (take Martha's pearls)
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == "__main__":
	main()
