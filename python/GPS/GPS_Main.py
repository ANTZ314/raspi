# -*- coding: utf-8 -*-
"""
Created on: 	[2017-05-09]
@author: 		Antony Smith
@description: 	Opens image at predefined location counts faces
				If file doesn't exist, creates file and appends
				image directory/name.jpg and number of faces counted

Run:			python GPS_Main.py
"""
import sys
import GPS_Class2 as GPS_Class

def main():
	try:
		GPS = GPS_Class.GPSClass()				# Create Instance of the class
		GPS.message("Message!")
		GPS.Get_GPS()
		
	# Ctrl+C will exit the program correctly
	except KeyboardInterrupt:
		#GPIO.cleanup()								# Only if GPIO's were used
		ser.close()									# close the serial connection
		print("\r\nEXIT PROGRAM!!")
		sys.exit(0)
    
if __name__ == "__main__": main()
