# -*- coding: utf-8 -*-
"""
Created by: 	A.Smith
Date:			2017-08-15
Description:	USB-Serial comms to uBlox NEO-M8T-Q-10
				Remove all other GPS NMEA string except $GPRMS
				Pring the respective extracted data from GNRMC string
String: TIME   V/A   COORD1  N/S  COORD2  E/W        DATE    ERROR
-------------------------------------------------------------------
$GNRMC,130331.00,A,2544.55942,S,02816.91443,E,0.098,,160817,,,A*76
-------------------------------------------------------------------
To list USB tty devices:
$ ls -l /dev/tty*
$ lsusb
$ usb-devices
"""
import serial
import sys
from time import sleep

class GPSClass:
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

	def __init__(self, **kwargs):
		print("Powering up!!")
		
	def message(self, string):
		print("Incoming {0}\n".format(str(string)))

	def Get_GPS(self):
		other = 'string'
		valid = 0										# check if GPRMS string valid
		count = 0										# block of RMS strings
		save  = 0										# save a single RMS string
		try:
			# set up the serial to USB data
			ser = serial.Serial(self.port, self.baud, timeout=1)
			# open the serial port
			if ser.isOpen():
				print(ser.name + ' is open...')			# display com port name
			
			# Eliminate other messages
			for rms in self.list:
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
				self.coord.append(sender)					# copy into array
				# At each special error check print string
				if sender == '*':						# look for error check char
					if save == 1:						# after every 5 coords
						save = 0						# clear flag
						# If coordinate Invalid character found
						if self.coord[9]:					# check invalid coordinates
							print('INVALID COORDINATES!!')	# incorrect kid!
							for i in range (0, 20):		# print tyhe incorrect string
								print(str(self.coord[i])),	# char by char due to encoding
							
						# If coordinate validation character found
						elif self.coord[16] == 'A':			# check for string validation
							print('VALID!!')			# Scream it from the mountain tops
							# Extract Data fields
							for i in range (6, 12):		# position in GNRMC string
								self.Time.append(self.coord[i])	# Time
							for i in range (18, 28):	# position in GNRMC string
								self.Lat.append(self.coord[i])	# Latitude
							for i in range (31, 42):	# position in GNRMC string
								self.Lon.append(self.coord[i])	# Longitude
							for i in range (52, 58):	# position in GNRMC string
								self.Date.append(self.coord[i])	# Date
							# Display the individual values
							Times = ''.join(self.Time)				# 
							print("TIME: {}".format(Times)),	# show single string
							Dates = ''.join(self.Date)				# 
							print("DATE: {}".format(Dates)),	# show single string
							Lats = ''.join(self.Lat)					# 
							print("LATITUDE: {}".format(Lats)),	# show single string
							Lons = ''.join(self.Lon)					# 
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
						del self.coord[:]					# clear array & get next line
						save = 1 						# Flag - get next single line $ -> *
		# Ctrl+C will exit the program correctly
		except KeyboardInterrupt:
			#GPIO.cleanup()								# Only if GPIO's were used
			ser.close()									# close the serial connection
			print("\r\nEXIT PROGRAM!!")
			sys.exit(0)									# kill Batmans parents in a dark alley
