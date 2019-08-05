# -*- coding: utf-8 -*-
"""
From:
https://tungweilin.wordpress.com/2015/01/04/python-serial-port-communication/
"""
import serial
from time import sleep

port = "COM5"
baud = 19200

list = ["$PUBX,40,GGA,0,0,0,0*5A",
		"$PUBX,40,GLL,0,0,0,0*5C",
		"$PUBX,40,VTG,0,0,0,0*5E",
		"$PUBX,40,GSV,0,0,0,0*59",
		"$PUBX,40,GSA,0,0,0,0*4E",
		"$PUBX,40,ZDA,0,0,0,0*44"]

def main():
	count = 0
	ser = serial.Serial(port, baud, timeout=1)
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
		print(out),
		if out == '*':
			if count == 10:
				count = 0
				cmd = raw_input("\nEnter command or 'exit':")
				if cmd == 'exit':
					ser.close()
					exit()
				else:
					print(cmd + " - continue...\r\n")
			else:
				count += 1

if __name__ == '__main__': main()
