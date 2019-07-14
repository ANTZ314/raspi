""" Raspberry Pi single LED test """

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
GPIO.setup(11, GPIO.OUT)  		# GPIO11 - BMC17 - WiringPi0
  
################################
## Do until program is exited ## 
################################
try:  
    print "Start loop"
    for i in range(0,10):
		blink(11)
	
#############################################################
## CTRL+C exit - Set all outputs to inputs to avoid damage ## 
#############################################################
finally:  							 	# when you CTRL+C exit, we clean up  
    GPIO.cleanup() 
