"""---------------------------------------------------------"""
""" Convert 1Byte (8-bit) value into binary output on GPIOs """
""" 				WIRING PI VERSION 03					"""
"""---------------------------------------------------------"""
import RPi.GPIO as GPIO  
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

def blink(pin):
	wiringpi.digitalWrite(pin, 0) 	# sets port 17 to 0 (0V, off)  
	sleep(0.2)  					# 0.5sec
	wiringpi.digitalWrite(pin, 1) 	# sets port 17 to 1 (3V3, on)  
	sleep(0.2)  					# 0.5sec  
	return
	
def data_Out(val):
	DBCnt = 0;
	Temp;
	LCD_Mask = 0x01;				# 0000 0001
	
	for num in range(8)						# loop 8 bit (1 byte)
		Temp = val;									// copy original each loop
		Temp &= LCD_Mask;								// Mask copy each loop
		
		# pin matching count = high #
		if Temp >= 0X01:
			digitalWrite(LCD_DB1[DBCnt], HIGH); 		// Turn LED[x] ON
		# pin matching count = low #
		else:
			digitalWrite(LCD_DB1[DBCnt], LOW); 			// Turn LED[x] OFF
		
		#LCD_Mask = LCD_Mask << 1;						// shift mask to next bit (double)
		LCD_Mask *= 2;									// shift mask to next bit (double)
		
	return

def main():
	var=1
	################################
	## Do until program is exited ## 
	################################
	try:  
		print "Start loop"
		blink(17)					# runtime check
		while var<=25 :				# loop 25 times thru all 8
			data_Out(0xAA)
			data_Out(0x55)			
			var += 1

	###############################################
	## Set all outputs to inputs to avoid damage ##
	###############################################
	finally:  							 	# when you CTRL+C exit, we clean up 
		print "\nDone!!"
		GPIO.cleanup() 
	return
	
if __name__ == "__main__":
	main()

