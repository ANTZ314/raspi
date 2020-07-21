# -*- coding: utf-8 -*-
"""
Description:
Integration of 'json1.py' (json string creator) and 'iot-pub.py' (gcloud publisher)

Notes:
ssl security files: roots.pem & rsa_private.pem
'jwt_maker.py' to create JWT security key

Use:
python iot-core.py
"""
import json
#from datetime import datetime
import datetime
import time
import jwt
import paho.mqtt.client as mqtt

## Define some project-based variables to be used below ##
ssl_private_key_filepath = './certs/rsa_private.pem'  # '<ssl-private-key-filepath>'
ssl_algorithm            = 'RS256'                    # '<algorithm>' # Either RS256 or ES256
root_cert_filepath       = './certs/roots.pem'        # '<root-certificate-filepath>'
project_id               = 'iot-omnigo1'              # '<GCP project id>'
gcp_location             = 'us-central1'              # '<GCP location>'
registry_id              = 'omnigo_registry'          # '<IoT Core registry id>'
device_id                = 'omnigo_device1'           # '<IoT Core device id>'


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
## STORE TO FILE 		##
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

	return jsonStr										# pass JSON string back

####################
## THE BIG KAHUNA ##
####################
def main():	
	qrData = "data from qr code"
	iotJSON = "upload"

	#############################################
	## Read "QR_Code" data - text file for now ##
	#############################################
	file = open('qrCode.txt', 'r')
	qrData = file.read()
	file.close()
	#############################################
	
	print("Create the JSON stuff...")
	iotJSON = createJSON(qrData)	# Ummmmm...?

	print("Publish the JSON string to GCP")
	iot_publish(iotJSON)			# Publish JSON to IoT_Core

	print("COMPLETE!!")



if __name__ == "__main__": main()