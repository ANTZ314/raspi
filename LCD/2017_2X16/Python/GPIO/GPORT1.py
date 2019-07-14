"""---------------------------------------------------------"""
""" Convert 1Byte (8-bit) value into binary output on GPIOs """
""" 				GPIO.RPI VERSION 01						"""
"""---------------------------------------------------------"""
import RPi.GPIO as GPIO  
import time 

# blinking function  
def blink(pin):  
        GPIO.output(pin,GPIO.HIGH)  
        time.sleep(0.5)  				# pause 1 sec
        GPIO.output(pin,GPIO.LOW)  
        time.sleep(0.5)  				# pause 1 sec
        return 

# to use Raspberry Pi board pin numbers  
GPIO.setmode(GPIO.BOARD)  
# set up GPIO output channel  
GPIO.setup(11, GPIO.OUT)  		# GPIO11 - BCM17 - WiringPi_00
GPIO.setup(13, GPIO.OUT)  		# GPIO13 - BCM27 - WiringPi_02
GPIO.setup(15, GPIO.OUT)  		# GPIO15 - BCM22 - WiringPi_03
GPIO.setup(19, GPIO.OUT)  		# GPIO19 - BCM10 - WiringPi_12
GPIO.setup(21, GPIO.OUT)  		# GPIO21 - BCM09 - WiringPi_13
GPIO.setup(23, GPIO.OUT)  		# GPIO23 - BCM11 - WiringPi_14
GPIO.setup(27, GPIO.OUT)  		# GPIO27 - BCM00 - WiringPi_30
GPIO.setup(29, GPIO.OUT)  		# GPIO29 - BCM05 - WiringPi_21
  
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
