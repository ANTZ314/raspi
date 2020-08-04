"""
Description:
Create blank Omnigo Data Object & fill in data
Convert Python Class Object to JSON string
"""
#import sys
import json

class OmniData:
	CLIENT_NAME_CODE = 'TSE'
	PROJECT_KIT_ID = 515151515
	STAGE = 'NULL'
	NUMBER_OF_BOARDS = 0
	NUMBER_OF_PANELS = 0
	STAFF_ID = 000
	TIME = '00:00'
	DATE = '01-01-2020'
	START = '00:00'
	STOP = '00:00'
	FAULT = 'NULL'
	SERIAL_NO = 121212121


def main():	
	#create object
	OmniData1 = OmniData()
	OmniData1.CLIENT_NAME_CODE = 'Omnigo'
	OmniData1.PROJECT_KIT_ID = 123456789
	OmniData1.STAGE = 'SMT'
	OmniData1.NUMBER_OF_BOARDS = 1000
	OmniData1.NUMBER_OF_PANELS = 50
	OmniData1.STAFF_ID = 456
	OmniData1.TIME = '12:35'
	OmniData1.DATE = '11-06-2020'
	OmniData1.START = '08:35'
	OmniData1.STOP = '00:00'
	OmniData1.FAULT = 'NULL'
	OmniData1.SERIAL_NO = 987654321

	#convert to JSON string
	jsonStr = json.dumps(OmniData1.__dict__)

	#print json string
	print(jsonStr)


if __name__ == "__main__": main()
