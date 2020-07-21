# -*- coding: utf-8 -*-
"""
Description:
Read from text file - which will be the QR Code scan
Fill in data feilds in the dictionary with QR data
Convert all data from dictionary to JSON format
Write to JSON file

NOTE: File CANNOT be called "json.py" -> causes error
"""
import json
from datetime import datetime

## Proiject Information dictionary ##
dataDict = {'CLIENT'	: 'xxx',			# Client Name
			'PROJECT'	: '0',				# Project ID
			'STAGE'		: 'xxx',			# Operational Stage (setup/smt/thru/insp)
			'BOARDS'	: '0',				# Number PC-Boards
			'PANELS'	: '0',				# Number of panels
			'STAFF_ID'	: '0',				# Staff member ID number
			'DATE'		: '00-00-2020',		# Project start date
			'TIME'		: '00:00',			# Time of each board swiped
			'START'		: '00:00',			# Stage - start time 
			'STOP'		: '00:00',			# Stage - end time
			'REASON'	: 'null',			# Reason the stage was stopped
			'SERIAL'	: '0' }				# Barcode serial number - Later


## DATA CLASS FOR JSON CONVERSION ##
class OmniData:
	CLIENT 	= 'TSE'
	PROJECT = 515151515
	STAGE 	= 'NULL'
	BOARDS 	= 0
	PANELS 	= 0
	STAFF_ID = 000
	DATE 	= '01-01-2020'
	TIME 	= '00:00'
	START 	= '00:00'
	STOP 	= '00:00'
	REASON 	= 'NULL'
	SERIAL 	= 121212121


## UPDATE ALL INFO DATA | CREATE JSON STRING | STORE TO FILE ##
def createJSON(qrData):
	exists = 0											# append after printing contents

	## Extract data with ',' delimiter - Directly into Global Disctionary ##
	dataDict = dict(i.split('=') for i in qrData.split(','))

	## Get Startup Information - Time & Date on 'SETUP' stage ##
	## At each Stage Start/Stop - Update Time ##
	now = datetime.now()								# Get 'nows' date & time
	#current_date = now.strftime("%Y-%m-%d")			# Extract date
	current_time = now.strftime("%H:%M:%S")				# Extract time

	## Depending on KIT or STAFF qrScan ##
	dataDict['START'] 	 = current_time					# insert current time
	dataDict['STOP'] 	 = current_time					# insert current time
	#dataDict['STAFF_ID'] = '159'						# everything in strings?

	#print(dataDict)									# REMOVE (view dictionary contents)

	## Use loop to import new data ##
	OmniData1 = OmniData()								# get object characteristics
	OmniData1.CLIENT 	= dataDict['CLIENT']
	OmniData1.PROJECT 	= dataDict['PROJECT']
	OmniData1.STAGE 	= dataDict['STAGE']
	OmniData1.BOARDS 	= dataDict['BOARDS']
	OmniData1.PANELS 	= dataDict['PANELS']
	OmniData1.STAFF_ID 	= dataDict['STAFF_ID']
	OmniData1.DATE 		= dataDict['DATE']
	OmniData1.TIME 		= dataDict['TIME']
	OmniData1.START 	= dataDict['START']
	OmniData1.STOP 		= dataDict['STOP']
	OmniData1.REASON 	= dataDict['REASON']
	OmniData1.SERIAL 	= dataDict['SERIAL']

	#convert to JSON string
	jsonStr = json.dumps(OmniData1.__dict__)
	#print(jsonStr)										# REMOVE (view json string)

	## Check if the file exists & OVER-WRITE new string ##
	try:												# Skip if file doesn't exist
		file = open('iotCore.json', 'r') 				# Open to read file
		#print (file.read())							# Print the contents
		file.close()									# Close the file
	except:
		exists = 1										# Don't append twice if file exists
		file= open("iotCore.json","w")					# Create/open file then Append data 
		#file= open("test.json","a+")					# Create/open file then Append data 
		file.write(jsonStr)								# 
		file.close()									# Exit the opened file

	# If file exists, append new string
	if exists == 0:										# append after printing contents
		file= open("iotCore.json","w")					# Create/open file then Append data 
		#file= open("test.json","a+")					# Create/open file then Append data 
		file.write(jsonStr)								# 
		file.close()									# Exit the opened file
	else:												# 
		print ("\nFile Didn't exist - Created???"	)				# notification	


## Send JSON file to Google IoTCore ##
def iotCore():
	print("Send to Google")



## THE BIG KAHUNA ##
def main():	
	qrData = "data from qr code"

	#############################################
	## Read "QR_Code" data - text file for now ##
	#############################################
	file = open('qrCode.txt', 'r')
	qrData = file.read()
	file.close()
	#############################################
	
	createJSON(qrData)

	iotCore()

	print("COMPLETE!!")



if __name__ == "__main__": main()