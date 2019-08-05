# -*- coding: utf-8 -*-
#
# Created on Tue Mar 28 10:53:06 2017
#
# @author: Jean Louw
#

# -------------------------------------IMPORTS----------------------------------
import json
import threading
import base64
# ------------------------------------------------------------------------------


# --------------------------------REPORT CLASS START----------------------------
class Report(object):

    # -------------------------------------------------------------------------#
    # Name: Report                                                             #
    # Function: This is the class in charge of all online and offline log      #
    #           and reporting of events such as errors, status, and events     #
    # Dependencies: json: for parsing and loading JSON strings                 #
    #               base64: for encoding audio data to be sent as string       #
    #               threading: for ensuring that calls don't clash             #
    # -------------------------------------------------------------------------#

# - - - - - - - - - - - - - - LOCAL STATIC DEFINES - - - - - - - - - - - - - - -

    __version__ = "2017.2"

# - - - - - - - - - - - - - - -  GENERAL FUNCTIONS - - - - - - - - - - - - - - -
    # <summary> Constructor function checks for dependent classes and sets uptime  </summary>
    # <param name="**kwargs"> Data passed into the object upon creation should include:
    #   sql_logger  = an object of type SQLog that will be used to store data locally
    #   api_logger  = an object of type APILog that will be used to store data online
    #   gps_data    = an object of type GPSData that will be used for time, signal, and location data
    #   module_data = an object of type ModuleData that will be used for internal unit monitoring
    def __init__(self, **kwargs):
        # initialize self.data dict
        self.data = kwargs
        # See if an instance of SQLog class is passed
        if self.data.get("sql_logger", None):
            print("SQLog Class Already Initialized")
        else:
            # if not, create an instance of SQLog
            import SQLog
            self.data["sql_logger"] = SQLog.SQLog()
            print("New SQLog Class Initialized")
        # See if an instance of APILog class is passed
        if self.data.get("api_logger", None):
            print("APILog Class Already Initialized")
        else:
            # if not, create an instance of APILog
            import APILog
            self.data["api_logger"] = APILog.APILog()
            print("New APILog Class Initialized")
        # Ensure that an instance of GPSDat class is passed
        if self.data.get("gps_data", None):
            print("GPSData Class Already Initialized")
        else:
            # if not, create an instance of GPSData
            import GPSDat
            self.data["gps_data"] = GPSDat.GPSData()
            print("New GPSData Class Initialized")
        # Ensure that an instance of ModuleDat class is passed
        if self.data.get("module_data", None):
            print("Module Data Class Already Initialized")
        else:
            # if not, create an instance of ModuleData
            import ModuleDat
            self.data["module_data"] = ModuleDat.ModuleData()
            print("New ModuleData Class Initialized")
        # After all of the classes are up and operational
        # set the time of this logging session's start
        self.data["uptime"] = self.data["gps_data"].current_time
        self.status_timer_started = False

    # <summary> Allows to reassign the active sub-class thread locks externally      </summary>
    # <param name="api_lock"> A threading.Lock() object passed to replace the original </param>
    # <note> This function is never used, deprecate in next version                     </note>
    def set_locks(self, api_lock, sql_lock):
        self.data["api_logger"].set_thread_lock(api_lock)
        self.data["sql_logger"].set_thread_lock(sql_lock)

# - - - - - - - - - - - - - - - REPORTING FUNCTIONS - - - - - - - - - - - - - -
    # <summary> Single-run function that attempts to synchronize online and local databases </summary>
    def report_all_unsent_data(self):
        print("   Reporting events:")
        self.report_unsent_events()
        print("   Reporting errors:")
        self.report_unsent_errors()
        print("   Reporting statuses:")
        self.report_unsent_statuses()
        print("   Reporting updates:")
        self.report_unsent_updates()

# - - - - - - - - - - - - - STATUS REPORTING FUNCTIONS - - - - - - - - - - - - -
    # <summary> This function, meant to be accessed externally, starts a timer that
    #           periodically attempts to upload a status report to the server API   </summary>
    def start_status_updates(self):
        self.status_timer_started = True
        self.data['status_report_timer'] = threading.Timer(10, self.report_status)
        self.data['status_report_timer'].start()

    # <summary> This function, meant to be accessed externally, stops the timer that
    #           periodically attempts to upload a status report to the server API    </summary>
    def stop_status_updates(self):
        # this variable merely keeps the timer from re-arming itself in report_status()
        self.status_timer_started = False

    # <status> Internal function in control of recording current unit status data
    #          in both SQL and API server databases                               </summary>
    def report_status(self):
        print("\n\nREPORTING STATUS\n\n")
        # first we create the dictionary that will be filled
        status_data = {}
        # ============== STATIC VALUES ===================
        # We start collating data with the static module_id
        if self.data.get("module_id", None):
            # note that module_id should be some kind of global or passed value
            status_data['module_id'] = self.data['module_id']
        else:
            status_data['module_id'] = 'no_id_specified'
        # the next is also the static value of module_name
        if self.data.get("module_name", None):
            status_data['module_name'] = self.data['module_name']
        else:
            status_data['module_name'] = 'no_name_specified'
        # a similar static value is to do with module version
        if self.data.get("module_version", None):
            status_data['module_version'] = self.data['module_version']
        else:
            status_data['module_version'] = 'no_version_specified'
        # lastly we have the static uptime set at init
        if self.data.get("uptime", None):
            status_data['uptime'] = self.data['uptime']
        else:
            status_data['uptime'] = self.data['gps_data'].current_time
        # ============== GPS DATA VALUES =================
        # date time string (dts) is the string value of the current time
        status_data['dts'] = self.data['gps_data'].current_time  # this is not a function but rather a decorator
        # gps_signal is string of the gps accuracy as a float
        status_data['gps_signal'] = self.data['gps_data'].gps_signal()
        # the decorator location_data returns a dictionary with module_longitude and module_longitude
        current_location = self.data['gps_data'].location_data
        # which we assign independently
        status_data['module_latitude'] = current_location['module_longitude']
        status_data['module_longitude'] = current_location['module_longitude']
        # signal_3g is a string of the GPRS signal strength in float form
        status_data['signal_3g'] = self.data['gps_data'].signal_3g()
        # ============= MODULE DATA VALUES ===============
        # network_usage returns a string of all the bytes sent and received in this session
        status_data['network_usage'] = self.data['module_data'].network_usage()
        # ip_address returns a string of the unit's ip on the active network connection
        status_data['ip_address'] = self.data['module_data'].ip_address()
        # ac_power is an integer representing the boolean value of whether the unit is powered
        status_data['ac_power'] = self.data['module_data'].ac_power()
        # battery_status is a string value that represent the battery's current charge/condition
        status_data['battery_status'] = self.data['module_data'].battery_status()
        status_data['cover_status'] = self.data['module_data'].cover_status()
        # storage_status is the string value of hard disk usage as a percentage value
        status_data['storage_status'] = self.data['module_data'].storage_status()
        # cpu_temp is a string value that represents the average temperature across all CPU's in degrees Centigrade
        status_data['cpu_temp'] = self.data['module_data'].cpu_temp()
        # ram is the string representation of the total utilized virtual memory as a percentage of the total
        status_data['ram'] = self.data['module_data'].ram()
        # cpu_utilization is a string of the most recent cpu usage as a percentage of the total
        status_data['cpu_utilization'] = self.data['module_data'].cpu_utilization
        # =============== SELF SET VALUES ================

        status_data['mic_status'] = str(self.microphone_functional)

        status_data['snr'] = str(self.microphone_snr)

        status_data['api_response'] = self.data["api_logger"].insert_status(status_data)

        self.data["sql_logger"].insert_Status_Log_table(status_data)
        print("\n\nSTATUS REPORTING DONE\n\n")

        # restart timer if set
        if self.data.get('status_report_timer', None) and self.status_timer_started:
            self.data['status_report_timer'] = threading.Timer(10, self.report_status)
            self.data['status_report_timer'].start()

    def report_unsent_statuses(self):
        for each_unupdated_record in self.data["sql_logger"].fetch_unsent_from_Status_Log_table():
            print("-> uploading status no " + str(each_unupdated_record['event_id']))
            status_data = {}

            # then we collate the data to send to the API endpoint
            if (self.data.get("module_id", None) != None):
                status_data['module_id'] = self.data['module_id']
            else:
                status_data['module_id'] = 'no_id_specified'

            if (self.data.get("module_name", None) != None):
                status_data['module_name'] = self.data['module_name']
            else:
                status_data['module_name'] = 'no_name_specified'

            if (self.data.get("module_version", None) != None):
                status_data['module_version'] = self.data['module_version']
            else:
                status_data['module_version'] = 'no_name_specified'

            status_data['dts'] = each_unupdated_record['dts']
            status_data['gps_signal'] = each_unupdated_record['gps_signal']
            status_data['signal_3g'] = each_unupdated_record['signal_3g']
            status_data['mic_status'] = each_unupdated_record['mic_status']
            status_data['snr'] = each_unupdated_record['snr']
            status_data['ac_power'] = each_unupdated_record['ac_power']
            status_data['network_usage'] = each_unupdated_record['network_usage']
            status_data['battery_status'] = each_unupdated_record['battery_status']
            status_data['cover_status'] = each_unupdated_record['cover_status']
            status_data['storage_status'] = each_unupdated_record['storage_status']
            status_data['cpu_temp'] = each_unupdated_record['cpu_temp']
            status_data['ram'] = each_unupdated_record['ram']
            status_data['cpu_utilization'] = each_unupdated_record['cpu_utilization']

            module_location = self.data['gps_data'].location_data
            status_data['module_latitude'] = module_location['module_longitude']
            status_data['module_latitude'] = module_location['module_longitude']
            status_data['ip_address'] = self.data['module_data'].ip_address()

            send_api_resp = self.data["api_logger"].insert_status(status_data)

            self.data["sql_logger"].update_Status_Log_table(event_id=each_unupdated_record['event_id'],
                                                            # the record to change
                                                            key='api_response',  # the item to change
                                                            value=send_api_resp)


# - - - - - - - - - - - - - UPDATE REPORTING FUNCTIONS - - - - - - - - - - - - -

# - - - - - - - - - - - - - EVENT REPORTING FUNCTIONS - - - - - - - - - - - - -

# - - - - - - - - - - - - - ERROR REPORTING FUNCTIONS - - - - - - - - - - - - -

    # <summary>
    def report_unsent_events(self):
        #first we loop through all of the unsent items in the events database
        for each_unupdated_record in self.data["sql_logger"].fetch_unsent_from_Event_Log_table():
            
            
            print("-> uploading event no " + str(each_unupdated_record['event_id']))
            event_data = {}

            event_file = open(each_unupdated_record['filepath'], "rb")
            event_data['audio_file'] = event_file.read()
            event_file.close()
            #then we collate the data to send to the API endpoint
            if (self.data.get("module_id", None)!=None): event_data['module_id'] = self.data['module_id']
            else: event_data['module_id'] = 'no_id_specified'
            
            if (self.data.get("module_name", None)!=None): event_data['module_name'] = self.data['module_name']
            else: event_data['module_name'] = 'no_name_specified'
            
            if (self.data.get("module_version", None)!=None): event_data['module_version'] = self.data['module_version']
            else: event_data['module_version'] = 'no_name_specified'
            
            event_data['gunshot_event'] = each_unupdated_record['gunshot_event']
            send_api_resp = self.data["api_logger"].insert_event(event_data)
            if(send_api_resp==201):
                import os
                os.unlink(each_unupdated_record['filepath'])
                self.data["sql_logger"].update_Event_Log_table(event_id = each_unupdated_record['event_id'],   #the record to change
                                                             key = 'filepath', #the item to change
                                                             value = '')    
            #finally we update the sql database with the response
            self.data["sql_logger"].update_Event_Log_table(event_id = each_unupdated_record['event_id'],   #the record to change
                                                         key = 'api_response', #the item to change
                                                         value = send_api_resp)  
                 
        
            
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
        live_event_data['api_response'] = self.data["api_logger"].insert_event(live_event_data)
        # After the return of the API response, we determine if we must save the data
        last_event_id = self.data["sql_logger"].last_Event_entry
        if last_event_id == None: last_event_id = 0
        else: last_event_id = last_event_id['event_id']
        this_event_id = last_event_id + 1
        if live_event_data['api_response'] != 201:   # if data is not sent
            event_file_name = str(this_event_id) + ".dat"
            newFile = open(event_file_name, "wb")
            newFile.write(live_event_data['audio_file'])
            live_event_data['filepath'] = event_file_name
            newFile.close()
        # Then we save the response to the local SQLite database
        self.data["sql_logger"].insert_Event_Log_table(live_event_data)
        # And we return whether the report was successful
        

    
        

    
            
            
    def report_unsent_errors(self):
        #first we loop through all of the unsent items in the events database
        for each_unupdated_record in self.data["sql_logger"].fetch_unsent_from_Error_Log_table():
            print("-> uploading error no " + str(each_unupdated_record['event_id']))
            error_data = {}
            #then we collate the data to send to the API endpoint
            if (self.data.get("module_id", None)!=None): error_data['module_id'] = self.data['module_id']
            else: error_data['module_id'] = 'no_id_specified'
            
            if (self.data.get("module_name", None)!=None): error_data['module_name'] = self.data['module_name']
            else: error_data['module_name'] = 'no_name_specified'
            
            if (self.data.get("module_version", None)!=None): error_data['module_version'] = self.data['module_version']
            else: error_data['module_version'] = 'no_name_specified'
            
            error_data['error_details'] = each_unupdated_record['error_details']
            send_api_resp = self.data["api_logger"].insert_error(error_data)
            #finally we update the sql database with the response
            self.data["sql_logger"].update_Error_Log_table(event_id = each_unupdated_record['event_id'],   #the record to change
                                                         key = 'api_response', #the item to change
                                                         value = send_api_resp)  
            
    
    def report_error(self, error_data):
        if (error_data.get("module_id", None)==None):
            if (self.data.get("module_id", None)!=None): error_data['module_id'] = self.data['module_id']
            else: error_data['module_id'] = 'no_id_specified'
        else: self.data['module_id'] = error_data['module_id']
            
        if (error_data.get("module_name", None)==None):
            if (self.data.get("module_name", None)!=None): error_data['module_name'] = self.data['module_name']
            else: error_data['module_name'] = 'no_name_specified'
        else: self.data['module_name'] = error_data['module_name']
            
        if (error_data.get("module_version", None)==None):
            if (self.data.get("module_version", None)!=None): error_data['module_version'] = self.data['module_version']
            else: error_data['module_version'] = 'no_name_specified'
        else: self.data['module_version'] = error_data['module_version']
        
        if (error_data.get("error_details", None)==None):
            if (self.data.get("error_details", None)!=None): error_data['error_details'] = self.data['error_details']
            else: error_data['error_details'] = 'no_details_specified'
        # When enough information is gathered to do an API upload, pass it through
        error_data['api_response'] = self.data["api_logger"].insert_error(error_data)
        # After the return of the API response, we collate more data
        if (error_data.get("error_date_time", None)==None):
            if (self.data.get("error_date_time", None)!=None): error_data['error_date_time'] = self.data['error_date_time']
            else: error_data['error_date_time'] = 'no_dts_specified' 
        # Then we save the response to the local SQLite database
        self.data["sql_logger"].insert_Error_Log_table(error_data)
        
    
    def report_unsent_updates(self):
        pass    
        
    def report_update(self, update_data):
        pass
        # First create a dictionary to store all the information
        
        # When enough information is gathered to do an API upload, pass it through
        
        # After the return of the API response, we collate more data
        
        # Then we save the response to the local SQLite database
        
    @property
    def microphone_functional(self):
        if not self.data.get("microphone_functional", None):
            self.data['microphone_functional'] = False
        return self.data['microphone_functional']

    @microphone_functional.setter
    def microphone_functional(self, bool_val):
        self.data['microphone_functional'] = bool_val

    @property
    def microphone_snr(self):
        if not self.data.get("microphone_snr", None):
            self.data['microphone_snr'] = 'snr_not_set'
        return self.data['microphone_snr']

    @microphone_snr.setter
    def microphone_snr(self, bool_val):
        self.data['microphone_snr'] = bool_val


def report_class_test_code():
    test_report_instance = Report(module_id='test_id',
                                  module_name='test name',
                                  module_version='test_version')
    test_report_instance.report_all_unsent_data()
    
if __name__ == "__main__":
    report_class_test_code()
