""" Raspberry Pi multiple GPIO test """

import RPi.GPIO as GPIO  
import time 

# blinking function  
def blink(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(1)  				# pause 1 sec
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(1)  				# pause 1 sec
        return 

# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  
# set up GPIO output channel  
GPIO.setup(11, GPIO.OUT)  		# GPIO11 - BCM17 - WiringPi_00
GPIO.setup(13, GPIO.OUT)  		# GPIO13 - BCM27 - WiringPi_02
GPIO.setup(15, GPIO.OUT)  		# GPIO15 - BCM22 - WiringPi_03
GPIO.setup(19, GPIO.OUT)  		# GPIO19 - BCM10 - WiringPi_12
  
################################
## Blink 4 bits 10 times each ## 
################################
try:  
    print "Start loop"
    for i in range(0,10):
		blink(11)
		blink(13)
		blink(15)
		blink(19)
	
###############################################
## Set all outputs to inputs to avoid damage ## 
###############################################
finally:  							 	# when you CTRL+C exit, we clean up  
    GPIO.cleanup() 
