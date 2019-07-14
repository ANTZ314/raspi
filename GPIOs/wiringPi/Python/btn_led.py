# -*- coding: utf-8 -*-
"""
@author: Antony Smith
@description: 
"""
# GPIO port numbers  
import wiringpi  
from time import sleep
import sys

GREEN1 	= 2						# RGB - Green
RED1	= 3						# RGB - Red
BLUE1 	= 4						# RGB - Blue
GREEN2 	= 17					# RGB - Green
RED2  	= 27					# RGB - Red
BLUE2	= 22					# RGB - Blue

# inupt = 0, output = 1, pwm = 2
wiringpi.wiringPiSetupGpio()  
wiringpi.pinMode(GREEN1, 1) 	# sets GPIO to output
wiringpi.pinMode(RED1, 1) 		# sets GPIO to output  
wiringpi.pinMode(BLUE1, 1) 		# sets GPIO to output 

def main():  
	# All off
	wiringpi.digitalWrite(GREEN1, 0)
	wiringpi.digitalWrite(RED1, 0)
	wiringpi.digitalWrite(RED1, 0)

	try:  
		while True:
			wiringpi.digitalWrite(GREEN1, 1) # sets port 24 to 0 (0V, off)  
			sleep(2)                    # wait 10s  
			wiringpi.digitalWrite(GREEN1, 0) # sets port 24 to 1 (3V3, on)  
			sleep(0.5)                    # wait 10s  

			wiringpi.digitalWrite(RED1, 1) # sets port 24 to 0 (0V, off)  
			sleep(2)                    # wait 10s  
			wiringpi.digitalWrite(RED1, 0) # sets port 24 to 1 (3V3, on)  
			sleep(0.5) 

			wiringpi.digitalWrite(BLUE1, 1) # sets port 24 to 0 (0V, off)  
			sleep(2)                    # wait 10s  
			wiringpi.digitalWrite(BLUE1, 0) # sets port 24 to 1 (3V3, on)  
			sleep(0.5) 

	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		print("\r\nEXIT PROGRAM!!")					# Pistol whip Thomas Wayne
		sys.exit(0)									# Take Martha's pearls

if __name__ == "__main__":	main()