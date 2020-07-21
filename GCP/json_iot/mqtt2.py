# -*- coding: utf-8 -*-
"""
Description:
Google Cloud IoT - MQTT publish to topic
Link:
https://stackoverflow.com/questions/49907529/google-cloud-iot-invalid-mqtt-publish-topic

Genrate Key Pair:
openssl req -x509 -newkey rsa:2048 -keyout rsa_private.pem -nodes -out rsa_cert.pem -subj "/CN=unused"

Get Google roots.pem file:
wget https://pki.google.com/roots.pem
"""
import paho.mqtt.client as mqtt
import ssl, random, jwt_maker
from time import sleep

root_ca     = '../certs/roots.pem'
public_crt  = '../certs/rsa_cert.pem'
private_key = '../certs/rsa_private.pem'

mqtt_url     = "mqtt.googleapis.com"
mqtt_port    = 8883
mqtt_topic   = "projects/iot-omnigo1/topics/omnigo_topic" #
project_id   = "iot-omnigo1"                              # 
cloud_region = "us-central1"                              # 
registry_id  = "omnigo_registry"                          # 
device_id    = "omnigo_device1"                           # 
#device_id    = "projects/iot-omnigo1/locations/us-central1/registries/omnigo_registry/devices/omnigo_device1"

connflag = False

def error_str(rc):
    """Convert a Paho error to a human readable string."""
    return "Some error occurred: {}: {}".format(rc, mqtt.error_string(rc))

def on_disconnect(unused_client, unused_userdata, rc):
    """Paho callback for when a device disconnects."""
    print("on_disconnect: ", error_str(rc))

def on_connect(client, userdata, flags, response_code):
    global connflag
    connflag = True
    print("Connected with status: {0}".format(response_code))

def on_publish(client, userdata, mid):
    print("User data: {0} -- mid: {1}".format(userdata, mid ))
    #client.disconnect()

if __name__ == "__main__":

    client = mqtt.Client("projects/{}/locations/{}/registries/{}/devices/{}".format(
                         project_id,
                         cloud_region,
                         registry_id,
                         device_id))

    client.username_pw_set(username='unused',
                           password=jwt_maker.create_jwt(project_id,
                                               private_key,
                                               algorithm="RS256"))

    client.tls_set(root_ca,
                   certfile = public_crt,
                   keyfile = private_key,
                   cert_reqs = ssl.CERT_REQUIRED,
                   tls_version = ssl.PROTOCOL_TLSv1_2,
                   ciphers = None)

    client.on_connect = on_connect
    client.on_publish = on_publish
    client.on_disconnect = on_disconnect

    print("Connecting to Google IoT Broker...")
    client.connect(mqtt_url, mqtt_port, keepalive=60)
    client.loop_start() 

    while True:
        sleep(0.5)
        print (connflag)
        if connflag == True:
            print("Publishing...")
            ap_measurement = random.uniform(25.0, 150.0)
            #payload = "sm1/sm1-payload-{}".format(ap_measurement)
            res = client.publish(mqtt_topic, ap_measurement, qos=1)
            if not res.is_published():
               print("Data not published!!")
            else:
               print("ActivePower published: %.2f" % ap_measurement)
        else:
            print("Waiting for connection...")
