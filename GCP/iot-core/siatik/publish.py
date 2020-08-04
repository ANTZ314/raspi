
import datetime
import jwt
import json
import requests
import base64
import os
import time
import threading

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='omnigo-5758861ef0c6.json'

def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            A JWT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """

    token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)

def publish(message_dict, stage):

    JWT_token = create_jwt('omnigo', 'rsa_private.pem', 'RS256')
    token = JWT_token.decode('utf8')

    message_string = json.dumps(message_dict)

    base64_message = base64.urlsafe_b64encode(bytes(message_string,'utf8'))

    message = {"binary_data": base64_message.decode('utf8')}

    payload = json.dumps(message)

    if stage == 'stage_0':
        url = 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-1:publishEvent'
    elif stage == 'stage_1':
        url = 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-2:publishEvent'
    elif stage == 'stage_2':
        url = 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-3:publishEvent'
    elif stage == 'stage_3':
        url = 'https://cloudiotdevice.googleapis.com/v1/projects/omnigo/locations/europe-west1/registries/omnigo-test/devices/omnigo-unit-4:publishEvent'

    headers = {
    'Authorization': 'Bearer {}'.format(token),
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text)

def stage_0(client_list):

    for client in client_list:
        start = True
        client_copy = client.copy()
        for i in range(client_copy.get("BOARDS")+1):
            if start == False:
                client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                if client_copy.get('SERIAL') == None:
                    client_copy['SERIAL'] = 0
                client_copy['SERIAL'] = client_copy.get('SERIAL')+1
                publish(client_copy,'stage_0')
            elif start:
                client_copy['STAGE'] = 'STAGE-0'
                client_copy['STAFF_ID'] = 597
                client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                client_copy['START'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                client_copy['DATE'] = str(datetime.datetime.today().strftime('%Y-%m-%d'))
                start = False
                publish(client_copy,'stage_0')
            time.sleep(10)
        client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
        client_copy['STOP'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
        client_copy['SERIAL'] = None
        client_copy['REASON'] = 'COMPLETE'
        publish(client_copy,'stage_0')

def stage_1(client_list):

    for client in client_list:
        start = True
        client_copy = client.copy()
        for i in range(client_copy.get("BOARDS")+1):
            if start == False:
                client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                if client_copy.get('SERIAL') == None:
                    client_copy['SERIAL'] = 0
                client_copy['SERIAL'] = client_copy.get('SERIAL')+1
                publish(client_copy,'stage_1')
            elif start:
                client_copy['STAGE'] = 'STAGE-1'
                client_copy['STAFF_ID'] = 423
                client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                client_copy['START'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                client_copy['DATE'] = str(datetime.datetime.today().strftime('%Y-%m-%d'))
                start = False
                publish(client_copy,'stage_1')
            time.sleep(10)
        client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
        client_copy['STOP'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
        client_copy['SERIAL'] = None
        client_copy['REASON'] = 'COMPLETE'
        publish(client_copy,'stage_1')

def stage_2(client_list):

    for client in client_list:
        start = True
        client_copy = client.copy()
        for i in range(client_copy.get("BOARDS")+1):
            if start == False:
                client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                if client_copy.get('SERIAL') == None:
                    client_copy['SERIAL'] = 0
                client_copy['SERIAL'] = client_copy.get('SERIAL')+1
                publish(client_copy,'stage_2')
            elif start:
                client_copy['STAGE'] = 'STAGE-2'
                client_copy['STAFF_ID'] = 121
                client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                client_copy['START'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                client_copy['DATE'] = str(datetime.datetime.today().strftime('%Y-%m-%d'))
                start = False
                publish(client_copy,'stage_2')
            time.sleep(10)
        client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
        client_copy['STOP'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
        client_copy['SERIAL'] = None
        client_copy['REASON'] = 'COMPLETE'
        publish(client_copy,'stage_2')

def stage_3(client_list):

    for client in client_list:
        start = True
        client_copy = client.copy()
        for i in range(client_copy.get("BOARDS")+1):
            if start == False:
                client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                if client_copy.get('SERIAL') == None:
                    client_copy['SERIAL'] = 0
                client_copy['SERIAL'] = client_copy.get('SERIAL')+1
                publish(client_copy,'stage_3')
            elif start:
                client_copy['STAGE'] = 'STAGE-3'
                client_copy['STAFF_ID'] = 313
                client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                client_copy['START'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
                client_copy['DATE'] = str(datetime.datetime.today().strftime('%Y-%m-%d'))
                start = False
                publish(client_copy,'stage_3')
            time.sleep(10)
        client_copy['TIME'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
        client_copy['STOP'] = str(datetime.datetime.today().strftime('%H:%M:%S'))
        client_copy['SERIAL'] = None
        client_copy['REASON'] = 'COMPLETE'
        publish(client_copy,'stage_3')

            

def simulate():

    client_project_list = [
        {
            "CLIENT": "Omnigo", 
            "PROJECT": 111111111, 
            "STAGE": None, 
            "BOARDS": 20, 
            "PANELS": 10, 
            "STAFF_ID": None, 
            "TIME": None,
            "DATE": None,  
            "START": None, 
            "STOP": None, 
            "REASON": None, 
            "SERIAL": None
        },
        {
            "CLIENT": "TSE", 
            "PROJECT": 222222222, 
            "STAGE": None, 
            "BOARDS": 20, 
            "PANELS": 10, 
            "STAFF_ID": None, 
            "TIME": None,
            "DATE": None,  
            "START": None, 
            "STOP": None, 
            "REASON": None, 
            "SERIAL": None
        },
        {
            "CLIENT": "DLC", 
            "PROJECT": 333333333, 
            "STAGE": None, 
            "BOARDS": 20, 
            "PANELS": 5, 
            "STAFF_ID": None, 
            "TIME": None,
            "DATE": None,  
            "START": None, 
            "STOP": None, 
            "REASON": None, 
            "SERIAL": None
        },
        {
            "CLIENT": "SIATIK", 
            "PROJECT": 444444444, 
            "STAGE": None, 
            "BOARDS": 20, 
            "PANELS": 10, 
            "STAFF_ID": None, 
            "TIME": None,
            "DATE": None,  
            "START": None, 
            "STOP": None, 
            "REASON": None, 
            "SERIAL": None
        }
    ]

    print("Run Thread 1")
    x = threading.Thread(target=stage_0, args=(client_project_list,))
    x.start()
    time.sleep(30)
    print("Run Thread 2")
    y = threading.Thread(target=stage_1, args=(client_project_list,))
    y.start()
    time.sleep(30)
    print("Run Thread 3")
    z = threading.Thread(target=stage_2, args=(client_project_list,))
    z.start()
    time.sleep(30)
    print("Run Thread 4")
    w = threading.Thread(target=stage_3, args=(client_project_list,))
    w.start()
    

if __name__ == "__main__":
    simulate()