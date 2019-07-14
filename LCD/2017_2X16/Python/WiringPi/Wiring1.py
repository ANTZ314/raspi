""" Created 8-bit Port for Raspberry Pi """
"""
import wiringpi
import time
io = wiringpi.GPIO(wiringpi.GPIO.WPI_MODE_PINS)

wiringpi.wiringPiSetupGpio()  
wiringpi.pinMode(24, 1)      # sets GPIO 24 to output 
"""

import wiringpi2 as wiringpi  
from time import sleep       # allows us a time delay 

wiringpi.wiringPiSetupGpio()  
wiringpi.pinMode(0, 1)      # sets GPIO 11 to output  
wiringpi.digitalWrite(0, 0) # sets port 11 to 0 (0V, off) 

var=1
################################
## Do until program is exited ## 
################################
try:  
    print "Start loop"
    while var==1 :
		wiringpi.digitalWrite(0, 0) 	# sets port 11 to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(0, 1) 	# sets port 11 to 1 (3V3, on)  
		sleep(5)  						# 5sec
	
#############################################################
## CTRL+C exit - Set all outputs to inputs to avoid damage ## 
#############################################################
finally:  							 	# when you CTRL+C exit, we clean up  
    wiringpi.digitalWrite(0, 0) 	 	# sets port 24 to 0 (0V, off)  
    wiringpi.pinMode(0, 0)      	 	# sets GPIO 24 back to input Mode 
