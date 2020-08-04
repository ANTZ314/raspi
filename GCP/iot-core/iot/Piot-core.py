# -*- coding: utf-8 -*-
"""
Description:
	Written for RasPi -> pyzbar + picamera
	Read QR Code (from text file), then copy data to Dictionary
	Create JSON string from disctionary
	Connect to GCP via MQTT and upload JSON string
	Converted to connect to SIATIK GCP project??

Notes:
	Due to python 2.7 versioning on RasPi Zero -> Dictionary is in jumbled order ? ? ?

GCP Requirements:
	-> ssl security files: 
		=> roots.pem
		=> rsa_private.pem
	-> 'jwt_maker.py' to create JWT security key

Use:
python iot-core.py
"""
## JSON File and GCP ##
#import datetime
import json
import time
import jwt
import paho.mqtt.client as mqtt

## QR CODE IMPORTS ##
from picamera import PiCamera		# Testing the Camera
from imutils.video import VideoStream	# Video access library
from pyzbar import pyzbar		# Decoding the QR Code
import datetime				# wekking?
import imutils 				# A little slice of Magic
import cv2				# When you stare into the matrix...

csv_file = "barcodes.csv"		# guess what this is?
"""
## GCP PROJECT VARIABLES - MINE ##
ssl_private_key_filepath = './certs/rsa_private.pem'  # '<ssl-private-key-filepath>'
ssl_algorithm            = 'RS256'                    # '<algorithm>' # Either RS256 or ES256
root_cert_filepath       = './certs/roots.pem'        # '<root-certificate-filepath>'
project_id               = 'iot-omnigo1'              # '<GCP project id>'
gcp_location             = 'us-central1'              # '<GCP location>'
registry_id              = 'omnigo_registry'          # '<IoT Core registry id>'
device_id                = 'omnigo_device1'           # '<IoT Core device id>'
"""
## GCP PROJECT VARIABLES - SIATIK ##
ssl_private_key_filepath = './certs/rsa_private.pem'		# '<ssl-private-key-filepath>'
ssl_algorithm            = 'RS256'                    		# '<algorithm>' -> Either RS256 or ES256
root_cert_filepath       = './certs/roots.pem'        		# '<root-certificate-filepath>'
project_id               = 'omnigo'              			# '<GCP project id>'
gcp_location             = 'europe-west1'              		# '<GCP location>'
registry_id              = 'omnigo-test'          			# '<IoT Core registry id>'
device_id                = 'omnigo-unit-1'           		# '<IoT Core device id>'


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

## Get the current time/date ##
cur_time = datetime.datetime.utcnow()


##############################
## CREATE THE JWT TOKEN KEY ##
##############################
def create_jwt():
  token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': project_id
  }

  with open(ssl_private_key_filepath, 'r') as f:
    private_key = f.read()

  return jwt.encode(token, private_key, ssl_algorithm)


##################################
## CONNECT VIA MQTT AND PUBLISH ##
##################################
def iot_publish(iotJSON):
    _CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id)
    _MQTT_TOPIC = '/devices/{}/events'.format(device_id)

    client = mqtt.Client(client_id=_CLIENT_ID)
    # authorization is handled purely with JWT, no user/pass, so username can be whatever
    client.username_pw_set(
        username='unused',
        password=create_jwt())

    def error_str(rc):
        return '{}: {}'.format(rc, mqtt.error_string(rc))

    def on_connect(unusued_client, unused_userdata, unused_flags, rc):
        print('on_connect', error_str(rc))

    def on_publish(unused_client, unused_userdata, unused_mid):
        print('on_publish')

    client.on_connect = on_connect
    client.on_publish = on_publish

    client.tls_set(ca_certs=root_cert_filepath) # Replace this with 3rd party cert if that was used when creating registry
    client.connect('mqtt.googleapis.com', 8883)
    client.loop_start()

    ## bullshit values ##
    temperature = 50
    humidity = 10
    pressure = 165

    for i in range(1, 11):
      temperature += i
      humidity += i
      pressure += i

      ## Payload = MY_JSON STRING ##
      #payload = '{{ "ts": {}, "temperature": {}, "pressure": {}, "humidity": {} }}'.format(int(time.time()), temperature, pressure, humidity)
      payload = iotJSON

      # Uncomment following line when ready to publish
      client.publish(_MQTT_TOPIC, payload, qos=1)

      print("{}\n".format(payload))

      time.sleep(1)

    client.loop_stop()


####################################
## DATA CLASS FOR JSON CONVERSION ##
####################################
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


##########################
## UPDATE ALL INFO DATA ## 
## CREATE JSON STRING 	## 
## STORE TO FILE 	##
##########################
def createJSON(qrData):
	exists = 0											# append after printing contents

	## Extract data with ',' delimiter - Directly into Global Disctionary ##
	dataDict = dict(i.split('=') for i in qrData.split(','))

	## Get Startup Information - Time & Date on 'SETUP' stage ##
	## At each Stage Start/Stop - Update Time ##
	now = datetime.datetime.now()								# Get 'nows' date & time
	#current_date = now.strftime("%Y-%m-%d")			# Extract date
	current_time = now.strftime("%H:%M:%S")				# Extract time

	## Depending on KIT or STAFF qrScan ##
	dataDict['START'] 	 = current_time					# insert current time
	dataDict['STOP'] 	 = current_time					# insert current time
	dataDict['STAFF_ID'] = '159'						# everything in strings?

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

	## convert to JSON string ##
	jsonStr = json.dumps(OmniData1.__dict__)
	#print(jsonStr)										# REMOVE (view json string)

	############################
	## REMOVED STRING STORAGE ##
	############################

	return jsonStr										# pass JSON string back


################
## QR SCANNER ##
################
def QR_Scan():
	init_time = time.time()				# no. of secs since 1 Jan 1970
	winName = "SCAN ID"				# name the video window
	scnCnt = 0									# Number of ID confirmations
	done = "n"									# Complete scanning flag
				
	## initialize video stream & warm up camera sensor
	print("[INFO] starting video stream...")
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)									# Allow video to stabalise
	cv2.namedWindow(winName)
	cv2.moveWindow(winName, 20,20)
				
	## open the output CSV file for writing
	csv = open(csv_file, "w")
	found = set()
	time.sleep(2.0)									# TEST - REMOVE??
	print("[INFO] csv file opened...")
				
	## Loop over the frames from the video stream #
	## Time-Out after 25 secs ##
	while time.time()-init_time < 25:
		## grab the frame from the threaded video stream and r
		## esize it to have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=400)
				 
		## find & decode the barcodes in each frame
		barcodes = pyzbar.decode(frame)

		## loop over the detected barcodes
		for barcode in barcodes:
			## extract bounding box location & draw around barcode
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
				 
			## the barcode data is a bytes object so if we want to draw it
			## on our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type
				 
			## draw the barcode data and barcode type on the image
			text = "{}".format(barcodeData)
			cv2.putText(frame, text, (x, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
				 
			## if barcode is not stored, update new one to CSV file
			if barcodeData not in found:
				#csv.write("{},{}\n".format(datetime.datetime.now(), barcodeData))
				csv.write("{}\n".format(barcodeData))
				csv.flush()
				found.add(barcodeData)
				#print("[INFO] ID not found.")
			else:
				#print("[INFO] ID: {}".format(barcodeData))
				#print("Scan no: {}\n".format(scnCnt))
				scnCnt += 1
						
			## If ID is confirmed 3 times?
			if scnCnt == 3:
				scnCnt = 0		# clear the counter
				done = "y"		# exit the loop

		## Show the output frame
		cv2.imshow(winName, frame)
		#cv2.imshow("SCAN ID", frame)
					
		key = cv2.waitKey(1) & 0xFF
				 
		## if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
		## if ID confirmed 3 times
		elif done == "y":
			break
				
	## close the output CSV file do a bit of cleanup
	print("[INFO] cleaning up...")
	csv.close()					# close excel document
	vs.stop()					# stop video stream
	cv2.destroyAllWindows()				# not destroying??
	#lift_window()					# Put GUI on the top
	return barcodeData


####################
## THE BIG KAHUNA ##
####################
def main():	
	qrData = "data from qr code"
	iotJSON = "upload"

	print("Read the QR Code...")
	#qrData = QR_Scan()
	#############################################
	## Read "QR_Code" data - text file for now ##
	#############################################
	file = open('qrCode.txt', 'r')
	qrData = file.read()
	file.close()
	#############################################
	print(qrData)
	
	print("Create the JSON stuff...")
	iotJSON = createJSON(qrData)			# self explanatory

	print("Publish the JSON string to GCP")
	iot_publish(iotJSON)					# Publish JSON to IoT_Core

	print("COMPLETE!!")


if __name__ == "__main__": main()
