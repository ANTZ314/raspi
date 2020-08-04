
###NOTES:
All devices are using the same private key to generate jwt tokens. 
The .pem file is included in the zip.

The publish.py file is the code used to simulate the devices from a laptop and can be useful as a reference.

Take note of the order the **"Key":"Value"** pairs are in. 
If the order is different the Dataflow will not be able to write the row to BigQuery.

 **Demo Dashboard:**
https://dashboard-jpnoxbw4eq-ew.a.run.app/

**Device urls:**

* 1: 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-1:publishEvent'

* 2: 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-2:publishEvent'

* 3: 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-3:publishEvent'

* 4: 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-4:publishEvent'


**GCP variables required for PiCode connectivity:**

	ssl_private_key_filepath = './certs/rsa_private.pem'		# '<ssl-private-key-filepath>'
	ssl_algorithm            = 'RS256'                    		# '<algorithm>' -> Either RS256 or ES256
	root_cert_filepath       = './certs/roots.pem'        		# '<root-certificate-filepath>'
	project_id               = 'omnigo'              			# '<GCP project id>'
	gcp_location             = 'europe-west1'              		# '<GCP location>'
	registry_id              = 'omnigo-test'          			# '<IoT Core registry id>'
	device_id                = 'omnigo-unit-1'           		# '<IoT Core device id>'

omnigo-unit-1:publishEvent
omnigo-unit-2:publishEvent
omnigo-unit-3:publishEvent
omnigo-unit-4:publishEvent
