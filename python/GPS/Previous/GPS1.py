# -*- coding: utf-8 -*-
"""
From:
https://tungweilin.wordpress.com/2015/01/04/python-serial-port-communication/
"""
import serial
from time import sleep

port = "COM5"
baud = 19200

def main():
	count = 0
	ser = serial.Serial(port, baud, timeout=1)
	# open the serial port
	if ser.isOpen():
		print(ser.name + ' is open...')
	
	# Eliminate other messages
	cmd = "$PUBX,40,GGA,0,0,0,0*5A"
	ser.write(cmd.encode('ascii')+'\r\n')
	out = ser.read()
	sleep(0.005)		# delay 5ms
	cmd = "$PUBX,40,GLL,0,0,0,0*5C"
	ser.write(cmd.encode('ascii')+'\r\n')
	out = ser.read()
	sleep(0.005)		# delay 5ms
	cmd = "$PUBX,40,VTG,0,0,0,0*5E"
	ser.write(cmd.encode('ascii')+'\r\n')
	out = ser.read()
	sleep(0.005)		# delay 5ms
	cmd = "$PUBX,40,GSV,0,0,0,0*59"
	ser.write(cmd.encode('ascii')+'\r\n')
	out = ser.read()
	sleep(0.005)		# delay 5ms
	cmd = "$PUBX,40,GSA,0,0,0,0*4E"
	ser.write(cmd.encode('ascii')+'\r\n')
	out = ser.read()
	sleep(0.005)		# delay 5ms
	cmd = "$PUBX,40,ZDA,0,0,0,0*44"
	ser.write(cmd.encode('ascii')+'\r\n')
	out = ser.read()
	sleep(0.005)		# delay 5ms

	while True:
		out = ser.read()
		#print(out, end="")			# python3
		print(out),					# python2
		

if __name__ == '__main__':
    main()
