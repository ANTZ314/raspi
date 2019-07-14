"""---------------------------------------------------------"""
""" Convert 1Byte (8-bit) value into binary output on GPIOs """
"""---------------------------------------------------------"""
import wiringpi2 as wiringpi  
from time import sleep       # allows us a time delay 

###########################
## DEFINE WIRINGPI GPIOs ##
###########################
wiringpi.wiringPiSetupGpio()  
# Broadcom pin 27, P1 pin 13
wiringpi.pinMode(0, 1)      # sets GPIO 11 to output 
wiringpi.digitalWrite(0, 0) # sets port 11 to 0 (0V, off)
# Broadcom pin 22, P1 pin 15
wiringpi.pinMode(2, 1)      # sets GPIO 13 to output  
wiringpi.digitalWrite(2, 0) # sets port 13 to 0 (0V, off)

var=1						# define variable

################################
## Do until program is exited ## 
################################
def blink():
	print "Start loop"
    while var==1 :
		wiringpi.digitalWrite(13, 1) 	# sets port 24 to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(13, 0) 	# sets port 24 to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		wiringpi.digitalWrite(15, 1) 	# sets port 24 to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(15, 0) 	# sets port 24 to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		
###############################################
## Set all outputs to inputs to avoid damage ##
############################################### 
def finished():
	wiringpi.digitalWrite(13, 0) 	 	# sets port to 0 (0V, off)  
    wiringpi.pinMode(13, 0)      	 	# sets GPIO back to input Mode  
    wiringpi.digitalWrite(15, 0) 	 	# sets port to 0 (0V, off)  
    wiringpi.pinMode(15, 0)      	 	# sets GPIO back to input Mode 
    
####################
## CALL FUNCTIONS ##
####################
blink()
finished()
