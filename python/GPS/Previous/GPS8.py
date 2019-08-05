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

To list USB tty devices:
$ ls -l /dev/tty*
$ lsusb
$ usb-devices
"""
import serial
import sys
from time import sleep

port = "/dev/ttyACM0"	# GPS
baud = 19200

coord = []
Time = []
Lat = []
Lon = []
Date = []
# GPS Deactivation Messages:
list = ["$PUBX,40,GGA,0,0,0,0*5A",
		"$PUBX,40,GLL,0,0,0,0*5C",
		"$PUBX,40,VTG,0,0,0,0*5E",
		"$PUBX,40,GSV,0,0,0,0*59",
		"$PUBX,40,GSA,0,0,0,0*4E",
		"$PUBX,40,ZDA,0,0,0,0*44"]

def main():
	other = 'string'
	valid = 0										# check if GPRMS string valid
	count = 0										# block of RMS strings
	save  = 0										# save a single RMS string
	try:
		ser = serial.Serial(port, baud, timeout=1)	# set up the serial to USB data
		# open the serial port
		if ser.isOpen():
			print(ser.name + ' is open...')			# display com port name
		
		# Eliminate other messages
		for rms in list:
			cmd = rms								# Get command		
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
			#67890123
			# At each special error check print string
			if sender == '*':						# look for error check char
				if save == 1:						# after every 5 coords
					save = 0						# clear flag
					# If coordinate Invalid character found
					if coord[9]:					# check invalid coordinates
						print('INVALID COORDINATES!!')	# incorrect kid!
						for i in range (0, 20):		# print tyhe incorrect string
							print(str(coord[i])),	# char by char due to encoding
						
					# If coordinate validation character found
					elif coord[16] == 'A':			# check for string validation
						print('VALID!!')			# Scream it from the mountain tops
						# Extract Data fields
						for i in range (6, 12):		# position in GNRMC string
							Time.append(coord[i])	# Time
						for i in range (18, 28):	# position in GNRMC string
							Lat.append(coord[i])	# Latitude
						for i in range (31, 42):	# position in GNRMC string
							Lon.append(coord[i])	# Longitude
						for i in range (52, 58):	# position in GNRMC string
							Date.append(coord[i])	# Date
						# Display the individual values
						Times = ''.join(Time)				# 
						print("TIME: {}".format(Times)),	# show single string
						Dates = ''.join(Date)				# 
						print("DATE: {}".format(Dates)),	# show single string
						Lats = ''.join(Lat)					# 
						print("LATITUDE: {}".format(Lats)),	# show single string
						Lons = ''.join(Lon)					# 
						print("LONGITUDE: {}".format(Lons)),# show single string
					
					cmd = raw_input("\nEnter command or 'exit':") # py3 input('')
					if cmd == 'q':					# can be 'exit'
						#GPIO.cleanup()				# Only if GPIO's were used
						ser.close()					# close the serial connection
						sys.exit(0)					# exit()
			# 5 (increase for accuracy) valid RMS string trigger
			elif sender == '$' and save == 0:		# check for valid coordinates
				count = 0							# clear start counter
				valid += 1							# valid counter
				if valid == 5:						# 5 valid coordinates
					valid = 0						# clean counter
					del coord[:]					# clear array & get next line
					save = 1 						# Flag - get next single line $ -> *
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		#GPIO.cleanup()								# Only if GPIO's were used
		ser.close()									# close the serial connection
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)									# kill Batmans parents in a dark alley

if __name__ == '__main__': main()
