""" Created 8-bit Port for Raspberry Pi """

import wiringpi2 as wiringpi  
from time import sleep       # allows us a time delay 

wiringpi.wiringPiSetupGpio()  
wiringpi.pinMode(24, 1)      # sets GPIO 24 to output  
wiringpi.digitalWrite(24, 0) # sets port 24 to 0 (0V, off) 

var=1
try:  
    print "Start loop"
    while var==1 :
		wiringpi.digitalWrite(24, 0) 	# sets port 24 to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(24, 1) 	# sets port 24 to 1 (3V3, on)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(24, 0) 	# sets port 24 to 0 (0V, off)  
		wiringpi.pinMode(24, 0)      	# sets GPIO 24 back to input Mode 
	
finally:  							 	# when you CTRL+C exit, we clean up  
    wiringpi.digitalWrite(24, 0) 	 	# sets port 24 to 0 (0V, off)  
    wiringpi.pinMode(24, 0)      	 	# sets GPIO 24 back to input Mode  
    # GPIO 25 is already an input, so no need to change anything
