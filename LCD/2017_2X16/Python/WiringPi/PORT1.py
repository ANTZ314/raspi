"""---------------------------------------------------------"""
""" Convert 1Byte (8-bit) value into binary output on GPIOs """
""" 				WIRING PI VERSION						"""
"""---------------------------------------------------------"""
import wiringpi2 as wiringpi  
from time import sleep       # allows us a time delay 

###########################
## DEFINE WIRINGPI GPIOs ##
###########################
wiringpi.wiringPiSetupGpio()  
# Broadcom pin 27, P1 pin 13
wiringpi.pinMode(17, 1)      # sets GPIO  to output 
wiringpi.digitalWrite(17, 0) # sets port  to 0 (0V, off)
# Broadcom pin 22, P1 pin 15
wiringpi.pinMode(27, 1)      # sets GPIO  to output  
wiringpi.digitalWrite(27, 0) # sets port  to 0 (0V, off) 
# Broadcom pin 10, P1 pin 19
wiringpi.pinMode(22, 1)      # sets GPIO  to output  
wiringpi.digitalWrite(22, 0) # sets port  to 0 (0V, off) 
# Broadcom pin 09, P1 pin 21
wiringpi.pinMode(10, 1)      # sets GPIO  to output  
wiringpi.digitalWrite(10, 0) # sets port  to 0 (0V, off) 
# Broadcom pin 11, P1 pin 23
wiringpi.pinMode(9, 1)      # sets GPIO  to output  
wiringpi.digitalWrite(9, 0) # sets port  to 0 (0V, off) 
# Broadcom pin 05, P1 pin 29
wiringpi.pinMode(11, 1)      # sets GPIO  to output  
wiringpi.digitalWrite(11, 0) # sets port  to 0 (0V, off) 
# Broadcom pin 06, P1 pin 31
wiringpi.pinMode(0, 1)      # sets GPIO  to output  
wiringpi.digitalWrite(0, 0) # sets port  to 0 (0V, off) 
# Broadcom pin 13, P1 pin 33
wiringpi.pinMode(5, 1)      # sets GPIO  to output  
wiringpi.digitalWrite(5, 0) # sets port  to 0 (0V, off) 

var=1

################################
## Do until program is exited ## 
################################
def blink():
	print "Start loop"
    while var==1 :
		## ALL ON ##
		wiringpi.digitalWrite(0, 1) 	# sets port  to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		wiringpi.digitalWrite(2, 1) 	# sets port  to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		wiringpi.digitalWrite(3, 1) 	# sets port  to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		wiringpi.digitalWrite(12, 1) 	# sets port  to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		wiringpi.digitalWrite(13, 1) 	# sets port  to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		wiringpi.digitalWrite(14, 1) 	# sets port  to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		wiringpi.digitalWrite(30, 1) 	# sets port  to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		wiringpi.digitalWrite(21, 1) 	# sets port  to 1 (3V3, on)  
		sleep(5)  						# 5sec 
		
		## ALL OFF ##
		wiringpi.digitalWrite(0, 0) 	# sets port  to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(2, 0) 	# sets port  to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(3, 0) 	# sets port  to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(12, 0) 	# sets port  to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(13, 0) 	# sets port  to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(14, 0) 	# sets port  to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(30, 0) 	# sets port  to 0 (0V, off)  
		sleep(5)  						# 5sec
		wiringpi.digitalWrite(21, 0) 	# sets port  to 0 (0V, off)  
		sleep(5)  						# 5sec
		
###############################################
## Set all outputs to inputs to avoid damage ##
############################################### 
def finished():
	wiringpi.wiringPiSetupGpio()  
	# Broadcom pin 27, P1 pin 13
	wiringpi.digitalWrite(0, 0)  # sets port 11 to 0 (0V, off)
	wiringpi.pinMode(0, 0)       # sets GPIO 11 to output 
	wiringpi.digitalWrite(2, 0)  # sets port 13 to 0 (0V, off) 
	wiringpi.pinMode(2, 0)       # sets GPIO 13 to output  
	wiringpi.digitalWrite(3, 0)  # sets port 15 to 0 (0V, off) 
	wiringpi.pinMode(3, 0)       # sets GPIO 15 to output  
	wiringpi.digitalWrite(12, 0) # sets port 19 to 0 (0V, off) 
	wiringpi.pinMode(12, 0)      # sets GPIO 19 to output  
	wiringpi.digitalWrite(13, 0) # sets port 21 to 0 (0V, off) 
	wiringpi.pinMode(13, 0)      # sets GPIO 21 to output  
	wiringpi.digitalWrite(14, 0) # sets port 23 to 0 (0V, off) 
	wiringpi.pinMode(14, 0)      # sets GPIO 23 to output  
	wiringpi.digitalWrite(30, 0) # sets port 27 to 0 (0V, off) 
	wiringpi.pinMode(30, 0)      # sets GPIO 27 to output  
	wiringpi.digitalWrite(21, 0) # sets port 29 to 0 (0V, off) 
	wiringpi.pinMode(21, 0)      # sets GPIO 29 to output   
###############################################

blink()
finished()
