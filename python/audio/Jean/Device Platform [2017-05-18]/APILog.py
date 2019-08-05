# -*- coding: utf-8 -*-
#
#Created on Fri Mar 10 12:33:25 2017
#
#@author: Jean Louw
#

#-------------------------------------IMPORTS----------------------------------
import requests
import json
import threading
#import datetime                     #date and time needs to be included on GPS
#import socket                       #this needs to be included on the GPS/main
#------------------------------------------------------------------------------

#-------------------------------APILOG CLASS START-----------------------------
class APILog(object):
    
    #-------------------------------------------------------------------------#
    # Name: APILog                                                            #
    # Function: Contains methods with which to log the gunshot application    #
    #           data for online server consumption through API endpoints.     #
    # Dependencies: json: for parsing and loading JSON strings                #
    #               request: for internet post and get requests               #
    #               threading: for ensuring that calls don't clash            #
    #-------------------------------------------------------------------------#
    
#- - - - - - - - - - - - - - LOCAL STATIC DEFINES - - - - - - - - - - - - - - -
    
    __version__ = "2017.4"
    
    # Details for AWS Server
    #_protocol = 'https://'
    #_host =  'https://snaw2tdcb6.execute-api.eu-west-1.amazonaws.com'
    
    # Details for lip-in.co.za Server
    #__protocol = 'http://'
    #_host = 'www.lip-in.co.za/gunshot'     
    
    # Details for lip-in.com Server
    _protocol = 'http://'
    _host = 'www.lip-in.com/gunshot'        
    
    # Details for localhost Server
    #__protocol = 'http://'
    #_host = 'localhost:8080/gunshot'       
    
    
    #These variables hold the URL endpoints to the API for post and get services
    _event_root = '/dev/api/module_event'
    _status_root = '/dev/api/module_status'
    _error_root = '/dev/api/module_error'
    _update_root = '/dev/api/module_update'
    
    
#- - - - - - - - - - - - - - - -HELPER FUNCTIONS- - - - - - - - - - - - - - - - 

    # <summary> Helper function for sending a simple GET request to a url </summary>
    # <param name="url"> The URL address that will receive the GET request  </param>
    # <returns> The HTTP result code (200, 404, etc.) for the sent request 
    #           If the request fails completely, returns 0                </returns>
    def get(self, url):
        with self.api_thread_lock:
            try:
                dat = requests.get(url,verify=False,timeout=3)
                res = dat.status_code
            except:
                res = 0
            return res
    
    # <summary> Helper function for sending a JSON loaded POST request to a url  </summary>
    # <param name="url"> The URL address that will receive the POST request        </param>
    # <param name="json"> A dictionary object that will be passed as the JSON body </param>
    # <returns> The HTTP result code (200, 404, etc.) for the sent request 
    #           If the request fails completely, returns 0                       </returns>        
    def post(self, url, json):
        with self.api_thread_lock:
            try:
                dat = requests.post(url, json = json, verify=False, timeout=3)
                res = dat.status_code
            except:
                res = 0
            return res
    
#- - - - - - - - - - - - - - -  GENERAL FUNCTIONS - - - - - - - - - - - - - - - 
        
    # <summary> Constructor function that merely creates a new thread lock </summary>
    def __init__(self):
        self.api_thread_lock = threading.Lock()
        
    # <summary> Allows to reassign the active thread lock externally                 </summary>
    # <param name="api_lock"> A threading.Lock() object passed to replace the original </param>
    def set_thread_lock(self, api_lock):
        self.api_thread_lock = api_lock    
        
    # <summary> Returns the currently active threading lock object </summary>
    # <returns> currently active threading.Lock() object           </returns>
    def get_thread_lock(self):
        return self.api_thread_lock

        
#- - - - - - - - - - - - - - - RETRIEVE FUNCTIONS - - - - - - - - - - - - - - -        
            

    # <summary> Generator that lists all the events logged online </summary>
    # <returns> Yields each event entry individually </returns>
    # <note> To fetch values, please note the variable names stored in insert_event </note>
    def list_event(self):
        res = self.get(self._protocol + self._host + self._event_root)
        if(res!=200): yield ("ERROR " + str(res))
        else:
            for events in json.loads(res.content):
                yield events    
                
    # <summary> Generator that lists all the statuses logged online </summary>
    # <returns> Yields each status entry individually </returns>
    # <note> To fetch values, please note the variable names stored in insert_status </note>
    def list_status(self):
        res = self.get(self._protocol + self._host + self._status_root)
        if(res!=200): yield ("ERROR " + str(res))
        else:
            for stat in json.loads(res.content):
                yield stat  
    
    # <summary> Generator that lists all the errors logged online </summary>
    # <returns> Yields each error entry individually </returns>
    # <note> To fetch values, please note the variable names stored in insert_error </note>
    def list_error(self):
        res = self.get(self._protocol + self._host + self._error_root)
        if(res!=200): yield ("ERROR " + str(res))
        else:
            for err in json.loads(res.content):
                yield err  
    
    # <summary> Generator that lists all the updates logged online </summary>
    # <returns> Yields each update entry individually </returns>
    # <note> To fetch values, please note the variable names stored in insert_update </note>
    def list_update(self):
        res = self.get(self._protocol + self._host + self._update_root)
        if(res!=200): yield ("ERROR " + str(res))
        else:
            for update in json.loads(res.content):
                yield update  
                
#- - - - - - - - - - - - - - - INSERT FUNCTIONS - - - - - - - - - - - - - - - -
    
    # <summary> Injects a single event record into the module_event API endpoint</summary>
    # <param name="event_info"> Receives a dictionary object with the following value names: 
    #   filepath = the STRING name value of the file that needs its data to be sent
    #   module_id = the STRING value of the unit's alphanumerical identification 
    #   module_longitude = the STRING value of the unit's geographic longitudinal coordinate
    #   module_latitude  = the STRING value of the unit's geographic latitudinal coordinate
    #   gunshot_event    = STRING value that is the JSON serialization of all the given 
    #                      information concerning the gunshot event
    #   audio_file       = Base64 formatted STRING of the the audio data passed
    # </param>
    # <returns> Returns true if successful or else returns false </returns>            
    def insert_event(self, event_info):
        # This line sends the post request to the endpoint in question
        resp = self.post(self._protocol + self._host + self._event_root, json = dict(event_info))
        #print("\nRESPONSE IS:\n" + str(resp) + "\nWITH HEAD OF:\n" + str(resp.headers) + "\nAND BODY OF\n" + str(resp.content))
        if resp != 201:         # A response of 201 means that the record
            print("Event Log Error")     # was created succesfully.
         #   print(resp.content)
        else: print("Event Logged Successfully")
        return resp
        
    # <summary> Injects a single status record into the module_status API endpoint</summary>
    # <param name="status_info"> Receives a dictionary object with the following value names: 
    #   module_id        = the STRING value of the unit's alphanumerical identification 
    #   module_name      = the STRING value of the unit's given name 
    #   module_version   = the STRING value of the unit's current version
    #   dts              = the STRING value of the current date and time at which the log occurs
    #   gps_signal       = an INTEGER value that represents the GPS signal level
    #   module_longitude = the STRING value of the unit's geographic longitudinal coordinate
    #   module_latitude  = the STRING value of the unit's geographic latitudinal coordinate
    #   signal_3g        = an INTEGER value that represents the 3G signal level
    #   mic_status       = an INTEGER value of 0 or 1 that represents the boolean value of its working status
    #   snr              = a STRING value that houses the float value of the microphone signal to noise ratio
    #   network_usage    = an INTEGER value that represents the current network usage value
    #   ip_address       = a STRING value holding the unit's IP address
    #   uptime           = the STRING value of the date and time at which the unit was turned on
    #   ac_power         = an INTEGER value of 0 or 1 that represents the boolean value of its AC powered status
    #   battery_status   = a STRING that describes the current status of the battery
    #   cover_status     = an INTEGER value of 0 or 1 that represents the boolean value of its covered status
    #   storage_status   = an INTEGER value of the remaining storage space on the unit
    #   cpu_temp         = an INTEGER value representing the current temperature of the unit
    #   ram              = an INTEGER value of the unit's current  memory utilization
    #   cpu_utilization  = an INTEGER value of the unit's current processing utilization
    # </param>
    # <returns> Returns true if successful or else returns false </returns>          
    def insert_status(self,status_info):
        # This line sends the post request to the endpoint in question
        resp = self.post(self._protocol + self._host + self._status_root, json = status_info)
        #print("\nRESPONSE IS:\n" + str(resp) + "\nWITH HEAD OF:\n" + str(resp.headers) + "\nAND BODY OF\n" + str(resp.content))
        if resp != 201:         # A response of 201 means that the record
            print("Status Log Error")       # was created succesfully.
           # print(resp.content)
        else: print("Status Logged Successfully")
        return resp
        
    # <summary> Injects a single error record into the module_error API endpoint</summary>
    # <param name="error_info"> Receives a dictionary object with the following value names: 
    #   module_id      = the STRING value of the unit's alphanumerical identification 
    #   module_name    = the STRING value of the unit's given name 
    #   module_version = the STRING value of the unit's current version
    #   error_details  = a STRING describing specifics of the error being logged
    # </param>
    # <returns> Returns true if successful or else returns false </returns>          
    def insert_error(self, error_info):
        # This line sends the post request to the endpoint in question
        resp = self.post(self._protocol + self._host + self._error_root, json = error_info)
        #print("\nRESPONSE IS:\n" + str(resp) + "\nWITH HEAD OF:\n" + str(resp.headers) + "\nAND BODY OF\n" + str(resp.content))
        if resp != 201:         # A response of 201 means that the record
            print("Error Log Error")        # was created succesfully.
          #  print(resp.content)
        else: print("Error Logged Successfully")
        return resp
    
    # <summary> Injects a single update record into the module_update API endpoint</summary>
    # <param name="**kwargs"> Receives coinciding parameters to the table column names: 
    #   updated_file_name      = the STRING name value of the file that was updated
    #   current_version        = the STRING value of the class' original version
    #   update_version         = the STRING value of the class' updated version
    #   update_start_date_time = STRING value of when the download started
    #   update_stop_date_time  = STRING value of whent the download ended
    #   update_status          = STRING stating if download has started, is busy or successful
    #   api_response           = the returned integer value from the attempt to upload to the API endpoint
    # </param>
    # <returns> Returns true if successful or else returns false </returns>          
    def insert_update(self, update_info, api_thread_lock):
        # This line sends the post request to the endpoint in question
        resp = self.post(self._protocol + self._host + self._update_root, json = update_info)
        #print("\nRESPONSE IS:\n" + str(resp) + "\nWITH HEAD OF:\n" + str(resp.headers) + "\nAND BODY OF\n" + str(resp.content))
        if resp != 201:         # A response of 201 means that the record
            print("Update Log Error")        # was created succesfully.
           # print(resp.content)
        else: print("Update Logged Successfully")
        return resp


#- - - - - - - - - - - - - - - - - -DECORATORS- - - - - - - - - - - - - - - - - 
        
    @property
    def thread_lock(self):
        return self.get_thread_lock()
        
    @thread_lock.setter
    def thread_lock(self, sqlock):
        self.set_thread_lock(sqlock)
        
#--------------------------------APILOG CLASS END------------------------------
        

#<summary>Test code for the class</summary>        
def APITestCode():
    #these imports are not to be called inside this class, but rather the parent
    import datetime
    import socket   
    #Dependant on the the above includes, these values are just to simulate real values that would be passed
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.connect(("lip-in.com",80)) #check if the connection is reliable/existant
    starttime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    # Frist you create a new instance of the API logging class
    instance_of_API = APILog()
    
    # When logging an error, a dictionary in the following form needs to be created
    error_info = {
                     'module_id' : 'mod_id_1000',
                     'module_name' : 'Gunshot Express',
                     'module_version' : 'v0.12',
                     'error_details' : 'Error details in STR'
                 }
    # The dictionary is then passed into the insert_error function of the APILog instance           
    result = instance_of_API.insert_error(error_info)
    if result == 201: print("SUCCESS") #the function returns True or False for created or not
    
    # When logging an event, a dictionary in the following form needs to be created
    event_info = {
                     'module_id' : 'test_module2',
                     'module_longitude' : '25.5559',
                     'module_latitude' : '-0.13435',
                     'gunshot_event' : '{"weapon": None,"shots_fired": 20,"duration" : "some time"}',
                     'audio_file' : "BASE64ENCODEDSTRINGOFFILEDATA"
                 }
    # The dictionary is then passed into the insert_event function of the APILog instance           
    result = instance_of_API.insert_event(event_info)
    if result == 201: print("SUCCESS") #the function returns True or False for created or not
    
    # When logging unit status, a dictionary in the following form needs to be created
    status_info = {  
                        "module_id":3,
                        "module_name":"test_module",
                        "module_version":"v1.0",
                        "dts":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                        "gps_signal":5,
                        "module_latitude":"-25.7468287",
                        "module_longitude":"28.2788928",
                        #"module_street_address":"CSIR, Meiring Naude Road",
                       # "module_city":"Pretoria",
                        "signal_3g":5,
                        "mic_status":int(True),
                        "snr":"1.20",
                        "network_usage":100,
                        "ip_address":s.getsockname()[0],
                        "uptime": starttime,
                        "ac_power":int(True),
                        "battery_status":"no battery",
                        "cover_status":int(True),
                        "storage_status":100,
                        "cpu_temp":30,
                        "ram":100,
                        "cpu_utilization":100,  
                    }
    # The dictionary object is then passed into the insert_status function of the APILog instance           
    result = instance_of_API.insert_status(status_info)
    if result == 201: print("SUCCESS") #the function returns True or False for created or not
    
    # When logging an update, a dictionary in the following form needs to be created
    update_info = {
                     'module_id' : 'test',
                     'module_name' : 'joe',
                     'module_previous_version' : 'oldAF',
                     'module_version' : 'newAF'
                  }
    # The dictionary object is then passed into the insert_update function of the APILog instance      
    result = instance_of_API.insert_update(update_info)
    if result == 201: print("SUCCESS") #the function returns True or False for created or not
    
    # Although they might be deprecated in the future, these functions list the records logged before
    for events in instance_of_API.list_event():
        print("\n\nEvent\n-----\n log_id = " + str(events['log_id'] + "\n module_id = " + str(events['module_id'])))
    for stat in instance_of_API.list_status():
        print("\n\nStatus\n-----\n log_id = " + str(stat['log_id'] + "\n module_id = " + str(stat['module_id'])))
    for update in instance_of_API.list_update():
        print("\n\nUpdate\n-----\n log_id = " + str(update['log_id'] + "\n module_id = " + str(update['module_id'])))
    for err in instance_of_API.list_error():
        print("\n\nError\n-----\n log_id = " + str(err['log_id'] + "\n module_id = " + str(err['module_id'])))
    
if __name__ == "__main__":APITestCode()