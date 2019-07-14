#######################
	WiringPi2-Python
#######################

import wiringpi2

#wiringpi2.wiringPiSetup() 		# For sequential pin numbering, one of these MUST be called before using IO functions
# OR
#wiringpi2.wiringPiSetupSys() 	# For /sys/class/gpio with GPIO pin numbering
# OR
wiringpi2.wiringPiSetupGpio() 	# For GPIO pin numbering

wiringpi2.pinMode(6,1) 			# Set pin 6 to 1 ( OUTPUT )
wiringpi2.digitalWrite(6,1) 	# Write 1 ( HIGH ) to pin 6
wiringpi2.digitalRead(6) 		# Read pin 6
