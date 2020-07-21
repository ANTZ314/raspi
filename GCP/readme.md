###Folder: GCP
* Functional integrated version of the below.
* Reads csv format string from the text file
* Stored each field of data to a dictionary
* converts dictionary to JSON format
* Stores string to JSON file
* Connects to Google IoT-Core via MQTT
* Transfers JSON string 11 times.


###Folder: json_iot
**iot-pub.py**

* Connects to Google IoT-Core via MQTT
* Transfers JSON string 11 times.

**json1.py** - 

* Reads csv format string from the text file
* Stored each field of data to a dictionary
* converts dictionary to JSON format
* Stores string to JSON file

**mqtt2.py**

* Connects to Google IoT-Core via MQTT
* never really took it further, but hopeful