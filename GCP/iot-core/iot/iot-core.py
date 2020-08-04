# -*- coding: utf-8 -*-
"""
Description:
	Linux test (virtualEnv = iot)
	RUN IN PYTHON 2.7 (RasPI)
	Read QR Code (from text file), then copy data to Dictionary
	Create JSON string from disctionary
	Connect to GCP via MQTT and upload JSON string
	Converted to connect to SIATIK GCP project??

Notes:
	Due to python 2.7 versioning on RasPi Zero -> Dictionary is in jumbled order ? ? ?
	Run in virtual env: source ~/virtualenvironment/iot/bin/activate

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
import datetime

"""
## GCP PROJECT VARIABLES - MINE ##
#ssl_private_key_filepath = './certs/rsa_private.pem'  	# '<ssl-private-key-filepath>'
ssl_private_key_filepath = './certs/rsa.pem'  			# '<ssl-private-key-filepath>'
ssl_algorithm            = 'RS256'                    	# '<algorithm>' # Either RS256 or ES256
root_cert_filepath       = './certs/roots.pem'        	# '<root-certificate-filepath>'
project_id               = 'iot-omnigo1'              	# '<GCP project id>'
gcp_location             = 'us-central1'              	# '<GCP location>'
registry_id              = 'omnigo_registry'          	# '<IoT Core registry id>'
device_id1               = 'omnigo_device1'           	# '<IoT Core device id>'
"""
## GCP PROJECT VARIABLES - SIATIK ##
ssl_private_key_filepath = './certs/rsa.pem'				# '<ssl-private-key-filepath>'
ssl_algorithm            = 'RS256'                    		# '<algorithm>' -> Either RS256 or ES256
root_cert_filepath       = './certs/roots.pem'        		# '<root-certificate-filepath>'
project_id               = 'omnigo'              			# '<GCP project id>'
gcp_location             = 'europe-west1'              		# '<GCP location>'
registry_id              = 'omnigo-test'          			# '<IoT Core registry id>'
device_id1               = 'omnigo-unit-1:publishEvent'		# '<IoT Core device id>'
device_id2               = 'omnigo-unit-2:publishEvent'		# '<IoT Core device id>'
device_id3               = 'omnigo-unit-3:publishEvent'		# '<IoT Core device id>'
device_id4               = 'omnigo-unit-4:publishEvent'		# '<IoT Core device id>'


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
    _CLIENT_ID = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(project_id, gcp_location, registry_id, device_id1)
    _MQTT_TOPIC = '/devices/{}/events'.format(device_id1)

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

    ## Publish string 5 times ##
    for i in range(1, 6):

      ## Payload = MY_JSON STRING ##
      payload = iotJSON

      # Uncomment following line when ready to publish
      client.publish(_MQTT_TOPIC, payload, qos=1)

      print("{}\n".format(payload))						# View the Payload

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


####################
## THE BIG KAHUNA ##
####################
def main():	
	qrData = "data from qr code"
	iotJSON = "upload"

	print("Read the QR Code...")
	#############################################
	## Read "QR_Code" data - text file for now ##
	#############################################
	file = open('qrCode.txt', 'r')
	qrData = file.read()
	file.close()
	#############################################
	#print(qrData)
	
	print("Create the JSON stuff...")
	iotJSON = createJSON(qrData)			# self explanatory

	print("Publish the JSON string to GCP")
	iot_publish(iotJSON)					# Publish JSON to IoT_Core

	print("COMPLETE!!")


if __name__ == "__main__": main()
