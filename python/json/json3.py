"""
Description:
Create blank Omnigo Data Object & fill in data
Convert Python Class Object to JSON string
Create JSON file if it doesn't exist
Append new JSON string to the file
"""
#import sys
import json
import sys

class OmniData:
	CLIENT_NAME = 'TSE'
	PROJECT_KIT_ID = 515151515
	STAGE = 'NULL'
	NO_OF_BOARDS = 0
	NO_OF_PANELS = 0
	STAFF_ID = 000
	TIME = '00:00'
	DATE = '01-01-2020'
	START = '00:00'
	STOP = '00:00'
	FAULT = 'NULL'
	SERIAL_NO = 121212121


def main():	
	exists = 0											# append after printing contents

	# New Data to Class Object
	OmniData1 = OmniData()
	OmniData1.CLIENT_NAME = 'Omnigo'
	OmniData1.PROJECT_KIT_ID = 123456789
	OmniData1.STAGE = 'SMT'
	OmniData1.NO_OF_BOARDS = 1000
	OmniData1.NO_OF_PANELS = 50
	OmniData1.STAFF_ID = 456
	OmniData1.TIME = '12:35'
	OmniData1.DATE = '11-06-2020'
	OmniData1.START = '08:35'
	OmniData1.STOP = '00:00'
	OmniData1.FAULT = 'NULL'
	OmniData1.SERIAL_NO = 987654321

	#convert to JSON string
	jsonStr = json.dumps(OmniData1.__dict__)

	#print(jsonStr)										#print json string

	# Check if the file exists & read contents
	try:												# Skip if file doesn't exist
		file = open('test.json', 'r') 					# Open to read file
		print (file.read())								# Print the contents
		file.close()									# Close the file
	except:
		exists = 1										# Don't append twice if file exists
		file= open("test.json","a+")					# Create/open file then Append data 
		file.write(jsonStr + "\n")								# 
		file.close()									# Exit the opened file

	# If file exists, append new string
	if exists == 0:										# append after printing contents
		file= open("test.json","a+")					# Create/open file then Append data 
		file.write(jsonStr + "\n")								# 
		file.close()									# Exit the opened file
	else:												# 
		print ("\nFile Didn't exist..."	)				# notification	



if __name__ == "__main__": main()
