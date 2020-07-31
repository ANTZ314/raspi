#IoT Core Setup:

###GC Platform:

[my_platform](https://console.cloud.google.com/iot/registries?folder=&organizationId=&project=iot-omnigo1&supportedpurview=project)


###RPi SETUP:

**Create & Activate Service Accounts:**

	gcloud auth login

	gcloud auth activate-service-account [ACCOUNT]

**RPI - Install Cloud SDK:**

Download SDK (LINK BELOW) -> Extract

**Run the script:**
./google-cloud-sdk/install.sh

**Run gcloud init to initialize the SDK:**
./google-cloud-sdk/bin/gcloud init


----------------------------------------------------------
RPI - GCloud info commands:
----------------------------------------------------------
If 'gcloud' doesn't work, use full path: "google-cloud-sdk/bin/gcloud"

	gcloud auth list
	gcloud config list
	gcloud info


**CGP - Create Device Registry:**

_IMAGE - 1 create device registry.png_


**Install the necessary packages:**

	pip3 install -r requirements.txt

**RPI - Generate a device key pair:**

Example [1]:

	openssl req -x509 -newkey rsa:2048 -keyout rsa_private.pem -nodes \
	    -out rsa_cert.pem -subj "/CN=unused"

Example [2]:

	openssl genpkey -algorithm RSA -out rsa_private.pem -pkeyopt rsa_keygen_bits:2048 
	openssl rsa -in rsa_private.pem -pubout -out rsa_public.pem

In 1 string:

	openssl genpkey -algorithm RSA -out rsa_private.pem -pkeyopt rsa_keygen_bits:2048 && openssl rsa -in rsa_private.pem -pubout -out rsa_public.pem


**Get the Google roots.pem file:**

Example [1]:

	wget https://pki.google.com/roots.pem

Example [2]:

	wget https://pki.goog/roots.pem

if ERROR:

	wget https://pki.google.com/roots.pem --no-check-certificate


**CGP - Add Device to Registry:**

_IMAGE - 2 add device registry.png_


**Publishing over the MQTT bridge:**

Py-Code in my Github

