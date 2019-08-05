# -*- coding: utf-8 -*-
#
# Created on Wed May 03 11:39:41 2017
#
# @author: Jean Louw (template)
#         Wayne Rabe


# -------------------------------------IMPORTS----------------------------------

from pyfirmata import Arduino
import psutil
import threading
# ------------------------------------------------------------------------------


# -----------------------------MODULE DATA CLASS START--------------------------
class ModuleData(object):
    
    # -------------------------------------------------------------------------#
    # Name: ModuleData                                                         #
    # Function: Contains methods with which to see all the values of the       #
    #           device itself, such as CPU temp etc.                           #
    # Dependencies: pyfirmata: for manipulating and reading Arduino pins       #
    #               psutil: for accessing network, disk, and memory info       #
    #               threading: for setting up a threaded timer function        #
    # -------------------------------------------------------------------------#
    
# - - - - - - - - - - - - - - LOCAL STATIC DEFINES - - - - - - - - - - - - - - -
    
    __version__ = "2017.0"

    MAX_VOLTAGE = 5.0       # this is the nominal input voltage for normal operation of the module
    USING_ARDUINO = False   # this tells the class whether or not Arduino is being used, default False

# - - - - - - - - - - - - - - -  GENERAL FUNCTIONS - - - - - - - - - - - - - - -
    
    def __init__(self, **kwargs):
        # initialize self.data
        self.data = kwargs
        # check to see if USING_ARDUINO was passed
        if self.data.get("USING_ARDUINO", None):
            # update the self value if USING_ARDUINO data is passed
            self.USING_ARDUINO = self.data['USING_ARDUINO']
        # based on USING_ARDUINO, set up comms
        if self.USING_ARDUINO:
            # set up Arduino comms
            self.board = Arduino('/dev/tty.usbserial-A6008rIF')  # NB! replace with real port number
            self.power_pin = self.board.get_pin('a:0:i')  # analog read
            self.cover_pin = self.board.get_pin('d:1:p')  # digital read
        # first value of cpu_percent is always 0 and should be ignored
        self.data['cpu_utilization'] = psutil.cpu_percent(interval=None)
        # set up timer function to update the cpu and other values continuously
        self.data['update_timer'] = threading.Timer(1, self.update_values)
        self.data['update_timer'].start()

# - - - - - - - - - - - - - - - -TIMER FUNCTIONS- - - - - - - - - - - - - - - -

    # <summary> Every time timer expires, updates some values and resets the timer </summary>
    def update_values(self):
        # update the cpu percentage value
        self.data['cpu_utilization'] = psutil.cpu_percent(interval=None)
        # reset the timer
        self.data['update_timer'] = threading.Timer(1, self.update_values)
        self.data['update_timer'].start()

# - - - - - - - - - - - - - - - -HELPER FUNCTIONS- - - - - - - - - - - - - - - -

    # <summary> If the unit is using an Arduino, it reads the power level           </summary>
    # <returns> power as a FLOAT of the current read voltage if Arduino is avalable
    #           or else returns defined MAX_VOLTAGE                                 </returns>
    def power_level(self):
        # As is known, Arduino converts voltage to 8 bit number, so it needs to be converted back.
        conversion_factor = self.MAX_VOLTAGE/255
        if self.USING_ARDUINO:
            power = self.power_pin.read()*conversion_factor
        else:
            power = self.MAX_VOLTAGE
        return power
        
# - - - - - - - - - - - - ARDUINO RETRIEVE FUNCTIONS - - - - - - - - - - - - - -

    # <summary> This function checks to see if the unit is self-powered </summary>
    # <returns> INTEGER value depicting the BOOLEAN value its self-powered state (True of False) </returns>
    def ac_power(self):
        # fetch the power level from the arduino/psutil and determine whether charging or not
        if self.power_level() >= 4.1:
            self.data['ac_power'] = True
        else:
            self.data['ac_power'] = False
        return int(self.data['ac_power'])  # returns an integer for use in all SQL Databases

    # <summary> This function returns the measured battery level if available </summary>
    # <returns> STRING value of the current battery state if sensor data is available
    #           or else return the value of "UNKNOWN:
    def battery_status(self):
        self.data['battery_status'] = "UNKNOWN"
        if self.USING_ARDUINO:
            # fetches the input voltage
            battery_level = self.power_level()
            # Depending on the level, give simple string returns
            if battery_level >= 4.1:
                self.data['battery_status'] = "Charging"
            elif battery_level >= 3.6:
                self.data['battery_status'] = "Full"
            elif battery_level >= 3.1:
                self.data['battery_status'] = "Low"
            elif battery_level >= 2.9:
                self.data['battery_status'] = "Empty"
            else:
                self.data['battery_status'] = "N/A"
        else:
            # In case the above method does not work, psutil sometimes also has a function for battery level
            if hasattr(psutil, "sensors_battery"):
                self.data['battery_status'] = str(psutil.sensors_battery().percent)
        return self.data['battery_status']

    # <summary> This function reads the Arduino pin for the open/closed status of the unit's cover </summary>
    # <returns> INTEGER value depicting the BOOLEAN state of the cover's open/closed status </returns>
    def cover_status(self):
        self.data['cover_status'] = True  # initialize for some return
        # The cover status can only be read by an io port available via ARDUINO
        if self.USING_ARDUINO:
            self.data['cover_status'] = self.cover_pin.read()
        return int(self.data['cover_status'])
     
        
# - - - - - - - - - - - - - DEVICE RETRIEVE FUNCTIONS - - - - - - - - - - - - -

    # <summary> Function that returns the percentage of hard disk space currently used </summary>
    # <returns> FLOAT value depicting the current percentage of used hard disk space </returns>
    def storage_status(self):
        # since windows differs in its representation of its root folder,
        # we fetch the disk usage data independantly
        if psutil.WINDOWS:
            self.data['storage_status'] = psutil.disk_usage('C:').percent
        else:
            self.data['storage_status'] = psutil.disk_usage('/').percent
        return str(self.data['storage_status'])
        
    # <summary> This function fetches the total amount of data used thus far</summary>
    # <returns> A STRING value of the total data used this session </returns>
    def network_usage(self):
        # fetch total data usage so far in this session in bytes
        self.data['network_usage'] = psutil.net_io_counters().bytes_recv + psutil.net_io_counters().bytes_sent
        return str(self.data['network_usage']) + ' bytes'

    # <summary> This function fetches the current outward facing IP address from socket </summary>
    # <returns> A STRING value with the unit's IP address as its content </returns>
    def ip_address(self):
        # first we reset the IP address to None so that we don't return nothing
        self.data['ip_address'] = "None"
        for pconn in psutil.net_connections():  # loop through all open connections
            if pconn.status == "ESTABLISHED":   # find the active internet connection
                self.data['ip_address'] = pconn.raddr[0]  # set the ip to that connection's
        return str(self.data['ip_address'])

    # <summary> This function uses psutil to fetch temperature of the cpu if available </summary>
    # <returns> FLOAT value representing the cpu_temperature in degrees Centigrade </returns>
    def cpu_temp(self):
        self.data['cpu_temp'] = 0.0
        if hasattr(psutil, "sensors_temperatures"):
            temps = psutil.sensors_temperatures()
            if temps:
                for entries in temps.items():  
                    for entry in entries:
                        if entry.current > self.data['cpu_temp']:
                            self.data['cpu_temp'] = entry.current
        return str(self.data['cpu_temp'])

    # <summary> This function uses psutil to fetch the used percentage of virtual memory </summary>
    # <returns> FLOAT value depicting the percentage of memory/ram used by the unit </returns>
    def ram(self):
        # fetch virtual memory as percentage
        self.data['ram'] = 100*psutil.virtual_memory().used/psutil.virtual_memory().total
        return str(self.data['ram'])

# - - - - - - - - - - - - - - - - - -DECORATORS- - - - - - - - - - - - - - - - -

    @property
    def cpu_utilization(self):
        return self.data['cpu_utilization']

# ------------------------------MODULE DATA CLASS END----------------------------


# <summary>Test code for the class</summary>
def module_test_code():
    # import time for sleep
    import time
    # create new instance of ModuleData
    mod = ModuleData()
    print("RAM% = " + str(mod.ram()))
    print("STORAGE% = " + str(mod.storage_status()))
    print("IP = " + str(mod.ip_address()))
    print("NET = " + str(mod.network_usage()))
    print("CPU TEMP = " + str(mod.cpu_temp()))
    for i in range(20):
        time.sleep(1)
        print("CPU% = " + str(mod.cpu_utilization))
    
    
if __name__ == "__main__":
    module_test_code()
