# -*- coding: utf-8 -*-
#
#Created on Thu Apr 06 11:45:27 2017
#
#@author: Jean Louw (template)
#         Wayne Rabe
#

#-------------------------------------IMPORTS----------------------------------

import datetime  #temporary
import socket    #temporary

#------------------------------------------------------------------------------

#-------------------------------GPS DATA CLASS START---------------------------
class GPSData(object):
    
    #-------------------------------------------------------------------------#
    # Name: GPSData                                                           #
    # Function: Contains methods with which to fetch data from the GPS module #
    #           concerning the time and location, among others, as well as    #
    #           some information concerning the GSM module.                   #
    # Dependencies: NOT YET DEFINED                                           #
    #-------------------------------------------------------------------------#    
    
#- - - - - - - - - - - - - - LOCAL STATIC DEFINES - - - - - - - - - - - - - - -
    
    __version__ = "2017.0"
    

#- - - - - - - - - - - - - - -  GENERAL FUNCTIONS - - - - - - - - - - - - - - -     
    
    # <summary> Constructor sets up communication to the GPS device </summary>
    def __init__(self, **kwargs):
        # initialize self.data
        self.data = kwargs
        # initialize internet socket data
        self.internet_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # initialize GPS socket data
        #
        # initialize time and location
        self.fetch_time();
        self.fetch_location();
        
#- - - - - - - - - - - - - - - RETRIEVE FUNCTIONS - - - - - - - - - - - - - - -      

        
    # <summary> This function fetches the current GPS accuracy level </summary>
    # <returns> A STRING value depicting the signal strength of the GPS </returns>
    def gps_signal(self):
        #fetch gps signal data
        self.data['gps_signal'] = 'updated_gps_signal'
        return str(self.data['gps_signal'])

    # <summary> This function fetches the current GPRS signal level </summary>
    # <returns> A STRING value depicting the signal strength of the GPRS </returns>
    def signal_3g(self):
        #fetch 3g signal data
        self.data['signal_3g'] = 'updated_gprs_signal'
        return str(self.data['signal_3g'])

    # <summary> Function to update the global current_time variable in STRING format </summary>    
    def fetch_time(self):
        #fetch the current time
       self.data['current_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        
    # <summary> Function to update the global module_longitude and module_latitude variables in STRING format </summary>      
    def fetch_location(self):
        #fetch the current location and converts it if need be
        self.data['module_longitude'] = "fetchlong"
        self.data['module_latitude']  = "fetchlat"
        

#- - - - - - - - - - - - - - - - - -DECORATORS- - - - - - - - - - - - - - - - - 

    @property
    def current_time(self):
        self.fetch_time()                   # first we update the current_time
        return self.data['current_time']    # then we return it

    @property 
    def location_data(self):
        self.fetch_location()                                               # first we update module_longitude and module_latitude
        location_data = {'module_longitude':self.data['module_longitude'],  # then we compile a dictionary with the values inside
                         'module_latitude' :self.data['module_latitude']}
        return location_data                                                # and finally we return the dictionary
        

#------------------------------GPS DATA CLASS END------------------------------

#<summary>Test code for the class</summary>
def GPSTestCode():
    #first create an instance of the GPSData class
    gps_dat = GPSData();
    #The following code represents how to fetch data from the instance:
    print("Current time is " + gps_dat.current_time)
    #Please note that the following can become decorators if more @properties are added for them
    print("Current GPRS signal is " + gps_dat.signal_3g())
    print("Current GPS signal is " + gps_dat.gps_signal())
    #remember that the location is returned as a dictionary to save cycles
    unit_location = gps_dat.fetch_location
    print("Current longitude is " + unit_location['module_longitude'])
    print("Current latitude is " + unit_location['module_latitude'])



if __name__ == "__main__":GPSTestCode()



