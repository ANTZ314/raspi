"""---------------------------------------------------------"""
""" Convert 1Byte (8-bit) value into binary output on GPIOs """
""" 				GPIO.RPI VERSION 01						"""
"""---------------------------------------------------------"""
import RPi.GPIO as GPIO  
import time 

def GPIO_Setup(pin):
	GPIO.setup(pin, GPIO.OUT)
	return

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
GPIO_Setup(11)
GPIO_Setup(13)
GPIO_Setup(15)
GPIO_Setup(19)
GPIO_Setup(21)
GPIO_Setup(23)
GPIO_Setup(27)
GPIO_Setup(29)
  
def main():
	################################
	## Blink 8 bits 10 times each ## 
	################################
	try:  
		print "Start loop"
		for i in range(0,10):
			blink(11)
			blink(13)
			blink(15)
			blink(19)
			blink(21)
			blink(23)
			blink(27)
			blink(29)
		
	###############################################
	## Set all outputs to inputs to avoid damage ## 
	###############################################
	finally:  							 	# when you CTRL+C exit, we clean up 
		GPIO.cleanup() 
	return
	
if __name__ == "__main__":
	main()
	
