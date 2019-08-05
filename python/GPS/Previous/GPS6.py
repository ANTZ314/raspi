# -*- coding: utf-8 -*-
"""
Created by: 	A.Smith
Date:			2017-08-15
Description:	USB-Serial comms to uBlox NEO-M8T-Q-10
				Remove all other GPS NMEA string except $GPRMS
String:
         TIME   V/A   COORD1  N/S  COORD2  E/W        DATE    ERROR
-------------------------------------------------------------------
$GNRMC,130331.00,A,2544.55942,S,02816.91443,E,0.098,,160817,,,A*76
$GNRMC,130332.00,A,2544.55938,S,02816.91442,E,0.098,,160817,,,A*79
-------------------------------------------------------------------
"""
import serial
import sys
from time import sleep

port = "COM5"	# Latte Panda
#port = "COM13"	# Windows PC
baud = 19200

coord = []
list = ["$PUBX,40,GGA,0,0,0,0*5A",
		"$PUBX,40,GLL,0,0,0,0*5C",
		"$PUBX,40,VTG,0,0,0,0*5E",
		"$PUBX,40,GSV,0,0,0,0*59",
		"$PUBX,40,GSA,0,0,0,0*4E",
		"$PUBX,40,ZDA,0,0,0,0*44"]

def main():
	other = 'string'
	valid = 0									# check if GPRMS string valid
	count = 0									# block of RMS strings
	save  = 0									# save a single RMS string
	ser = serial.Serial(port, baud, timeout=1)	# set up the serial to USB data
	# open the serial port
	if ser.isOpen():
		print(ser.name + ' is open...')			# display com port name
	
	# Eliminate other messages
	for rms in list:
		cmd = rms								# Get command
		#sender = cmd.encode('ascii')			
		#end2 = end1.encode('ascii')			
		#ser.write(sender + end2)				
		ser.write(cmd.encode('ascii')+'\r\n')	# convert to ASCII [ERROR]
		out = ser.read()						# output to GPS
		sleep(0.005)							# delay 5ms

		#sleep(0.5)
	while True:
		out = ser.read()						# get the unicode byte		
		## python 2.7 ##
		sender = out.decode("utf-8", "ignore")	# 
		#print('{0}'.format(sender)),			# 
		coord.append(sender)					# copy into array
		
		# At each special error check print string
		if sender == '*':
			if count == 16:						# offer quit at each 16 lines
				count = 0						# reset exit counter
				cmd = raw_input("\nEnter command or 'exit':") # py3 input('')
				if cmd == 'q':					# can be 'exit' 
					ser.close()					# close the serial connection
					sys.exit(0)
				else:
					#print("{}".format(coord)),
					print('\r\n WHOLE ARRAY \r\n ')
			else:
				count += 1						# Batmans balls
			if save == 1:
				save = 0						# clear flag
				GPRMS = ''.join(coord)
				print("HERE: {}".format(GPRMS)),		# show single string
				cmd = raw_input("\nEnter command or 'exit':") # py3 input('')
				if cmd == 'q':					# can be 'exit' 
					ser.close()					# close the serial connection
					sys.exit()					# exit()
		# 5 (increase for accuracy) valid RMS string trigger
		elif sender == '$' and save == 0:		# check for valid coordinates
			count = 0							# clear start counter
			valid += 1							# valid counter
			if valid == 5:						# 5 valid coordinates
				valid = 0						# clean counter
				del coord[:]					# clear array & get next line
				save = 1 						# Flag - get next single line $ -> *

if __name__ == '__main__': main()