
"""
Description:
Simple MQTT publisher
Restructured version for integration

Edited version of "GCP_Quick_Starts" example
License - http://www.apache.org/licenses/LICENSE-2.0

Notes:
requires ssl security files

Use:
python iot-pub.py
""" 

#!/usr/bin/python

#from sense_hat import SenseHat
import datetime
import time
import jwt
import paho.mqtt.client as mqtt


# Define some project-based variables to be used below. This should be the only
# block of variables that you need to edit in order to run this script

ssl_private_key_filepath = './certs/rsa_private.pem'  # '<ssl-private-key-filepath>'
ssl_algorithm            = 'RS256'                    # '<algorithm>' # Either RS256 or ES256
root_cert_filepath       = './certs/roots.pem'        # '<root-certificate-filepath>'
project_id               = 'iot-omnigo1'              # '<GCP project id>'
gcp_location             = 'us-central1'              # '<GCP location>'
registry_id              = 'omnigo_registry'          # '<IoT Core registry id>'
device_id                = 'omnigo_device1'           # '<IoT Core device id>'

# end of user-variables

cur_time = datetime.datetime.utcnow()

def create_jwt():
  token = {
      'iat': cur_time,
      'exp': cur_time + datetime.timedelta(minutes=60),
      'aud': project_id
  }

  with open(ssl_private_key_filepath, 'r') as f:
    private_key = f.read()

  return jwt.encode(token, private_key, ssl_algorithm)


def iot_publish():
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
      payload = '{{ "ts": {}, "temperature": {}, "pressure": {}, "humidity": {} }}'.format(int(time.time()), temperature, pressure, humidity)

      # Uncomment following line when ready to publish
      client.publish(_MQTT_TOPIC, payload, qos=1)

      print("{}\n".format(payload))

      time.sleep(1)

    client.loop_stop()

## THE BIG KAHUNA ##
def main():
  
  iot_publish()



  print("COMPLETE!!")



if __name__ == "__main__": main()