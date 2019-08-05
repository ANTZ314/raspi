# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 10:53:06 2017

@author: Jean Louw
"""
import json

import base64

class Report(object):
    
    def __init__(self, **kwargs):
        self.data = kwargs
        if (self.data.get("sqlogger", None)!=None):print("SQLog Class Already Initialized")
        else: 
            import SQLog
            self.data["sqlogger"] = SQLog.SQLog()
            print("New SQLog Class Initialized")
        if (self.data.get("apilogger", None)!=None): print("APILog Class Already Initialized")
        else: 
            import APILog
            self.data["apilogger"] = APILog.APILog()
            print("New APILog Class Initialized")
    
         
    def set_locks(self, api_lock, sql_lock):
        self.data["apilogger"].set_thread_lock(api_lock)
        self.data["sqlogger"].set_thread_lock(sql_lock)
        
            
    def report_all_unsent_events(self):
        pass
            
    def report_live_event(self, live_event_data):
        # We first strip
        # Chunk is the passed raw sound data from the gunshot event
        chunk = live_event_data.get('chunk', None)
        if chunk != None:
            # The chunck data has to be converted and stored in the understood 'audio_file' element
            live_event_data['audio_file'] = base64.b64encode(chunk)
            # Then the original chunk needs to be deleted because it cannot be sent
            del live_event_data['chunk']
        else: live_event_data['audio_file'] = None

        # Gunshot event data needs to be converted into json that can be sent
        live_event_data['gunshot_event'] = json.dumps(live_event_data['gunshot_event'] )
        # Insert generic data from class initialization:
        # Insert module_id
        if (live_event_data.get("module_id", None)==None):
            if (self.data.get("module_id", None)!=None): live_event_data['module_id'] = self.data['module_id']
            else: live_event_data['module_id'] = 'no_id_specified'
        # Insert module_longitude
        if (live_event_data.get("module_longitude", None)==None):
            if (self.data.get("module_longitude", None)!=None): live_event_data['module_longitude'] = self.data['module_longitude']
            else: live_event_data['module_longitude'] = 'no_long_specified'
        # Insert module_latitude
        if (live_event_data.get("module_latitude", None)==None):
            if (self.data.get("module_latitude", None)!=None): live_event_data['module_latitude'] = self.data['module_latitude']
            else: live_event_data['module_latitude'] = 'no_lat_specified'
        
        
        # When enough information is gathered to do an API upload, pass it through
        live_event_data['api_response'] = self.data["apilogger"].insert_event(live_event_data)
        # After the return of the API response, we determine if we must save the data
        last_event_id = self.data["sqlogger"].last_Event_entry
        if last_event_id == None: last_event_id = 0
        else: last_event_id = last_event_id['event_id']
        this_event_id = last_event_id + 1
        if live_event_data['api_response'] != 201:   # if data is not sent
            event_file_name = str(this_event_id) + ".dat"
            newFile = open(event_file_name, "wb")
            newFile.write(live_event_data['audio_file'])
            live_event_data['filepath'] = event_file_name
        # Then we save the response to the local SQLite database
        self.data["sqlogger"].insert_Event_Log_table(live_event_data)
        # And we return whether the report was successful
        
    def report_saved_event(self, saved_event_data):
        pass
        # First create a dictionary to store all the information
        self.event_data = {}
        
        # When enough information is gathered to do an API upload, pass it through
        
        # After the return of the API response, we collate more data
        
        # Then we save the response to the local SQLite database
    
        
    def report_all_unsent_statuses(self):
        pass
        
    def report_status(self, status_data):
        pass
        # First create a dictionary to store all the information
        
        # When enough information is gathered to do an API upload, pass it through
        
        # After the return of the API response, we collate more data
        
        # Then we save the response to the local SQLite database
    
    def report_all_unsent_errors(self):
        pass    
    
    def report_error(self, error_data):
        pass
        # First create a dictionary to store all the information
        
        # When enough information is gathered to do an API upload, pass it through
        
        # After the return of the API response, we collate more data
        
        # Then we save the response to the local SQLite database
    
    def report_all_unsent_events(self):
        pass    
        
    def report_update(self, update_data):
        pass
        # First create a dictionary to store all the information
        
        # When enough information is gathered to do an API upload, pass it through
        
        # After the return of the API response, we collate more data
        
        # Then we save the response to the local SQLite database
        
    
def ReportClassTestCode():
    
    from SQLog import SQLog
    from APILog import APILog
    #import ossaudiodev
    
    #import pip

    #pip.main(['install', 'pyaudio'])
    
    passing_SQLog_instance = SQLog(filename = "reptest.db")
    passing_APILog_instance = APILog()
    
    report_test_instance = Report(sqlogger = passing_SQLog_instance, 
                                  apilogger = passing_APILog_instance)
    
    
if __name__ == "__main__": ReportClassTestCode()