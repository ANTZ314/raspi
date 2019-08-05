# -*- coding: utf-8 -*-
"""
Created by: 	A.Smith
Date:			2017-08-15
Description:	USB-Serial comms to uBlox NEO-M8T-Q-10
				Remove all other GPS NMEA string except $GPRMS
"""
import serial
import sys
from time import sleep

port = "COM5"	# Latte Panda
#port = "COM13"	# Windows PC
baud = 19200

coord = [6]
list = ["$PUBX,40,GGA,0,0,0,0*5A",
		"$PUBX,40,GLL,0,0,0,0*5C",
		"$PUBX,40,VTG,0,0,0,0*5E",
		"$PUBX,40,GSV,0,0,0,0*59",
		"$PUBX,40,GSA,0,0,0,0*4E",
		"$PUBX,40,ZDA,0,0,0,0*44"]

def main():
	end1 = '\r\n'
	count = 0
	pos = 0
	ser = serial.Serial(port, baud, timeout=1)
	# open the serial port
	if ser.isOpen():
		print(ser.name + ' is open...')
	
	# Eliminate other messages
	for rms in list:
		cmd = rms								# Get command
		ser.write(cmd.encode('ascii')+'\r\n')	# convert to ASCII [ERROR]
		out = ser.read()						# output to GPS
		sleep(0.005)							# delay 5ms

	while True:
		out = ser.read()						# get the unicode byte
		
		## python 3.6 ##
		#sender = out.decode("utf-8", "ignore")	# convert back to character
		#print('{0}'.format(sender), end="")		
		#coord.append(sender) 					# Copy char to string array
		
		## python 2.7 ##
		sender = out.decode("utf-8", "ignore")
		print(out),							 	# show character 
		#print('{0}'.format(sender), end="")
		coord.append(sender)					# copy into array
		#pos += 1 								# increment position
		
		# at each special error check print string
		if sender == '*':
			pos = 0 							# clear position counter
			if count == 16:						# offer quit at each 10 lines
				count = 0						# reset exit counter
				cmd = raw_input("\nEnter command or 'exit':") # py3 input('')
				if cmd == 'q':					# can be 'exit' 
					ser.close()					# close the serial connection
					exit()						# exit -> sys.exit(0)
				else:
					#print("-* {} *-\r\n".format(coord))	#
					print(coord)	# print the string - python2
					
			else:
				count += 1

if __name__ == '__main__': main()
