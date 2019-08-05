# -*- coding: utf-8 -*-
"""
From Gunshot, edited for RasPi
To list USB tty devices:
$ ls -l /dev/tty*
$ lsusb
$ usb-devices
"""
import serial
from time import sleep

#port = "/dev/ttyAMA0" 	# Keyboard
port = "/dev/ttyACM0"	# GPS
#ser = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
baud = 19200

list = ["$PUBX,40,GGA,0,0,0,0*5A",
		"$PUBX,40,GLL,0,0,0,0*5C",
		"$PUBX,40,VTG,0,0,0,0*5E",
		"$PUBX,40,GSV,0,0,0,0*59",
		"$PUBX,40,GSA,0,0,0,0*4E",
		"$PUBX,40,ZDA,0,0,0,0*44"]

def main():
	count = 0
	try:
		ser = serial.Serial(port, baud, timeout=3.0)
		# open the serial port
		if ser.isOpen():
			print(ser.name + ' is open...')
		
		# Eliminate other messages
		for rms in list:
			cmd = rms								# Get command 
			ser.write(cmd.encode('ascii')+'\r\n')	# convert to ASCII
			out = ser.read()						# output to GPS
			sleep(0.005)							# delay 5ms

		while True:
			out = ser.read()
			#print(out, end="")						# python3
			print(out),								# python2
		
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		GPIO.cleanup()		# kill Batmans parents in a dark alley
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)

if __name__ == '__main__': main()
