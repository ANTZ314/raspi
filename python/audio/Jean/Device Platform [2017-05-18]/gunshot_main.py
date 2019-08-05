# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:28:58 2017

@author: Jean Louw
"""

import imports                       #this ensures all of the modules are installed for proper function
from Report import Report
from Record import Record
from SQLog import SQLog
from APILog import APILog
from GPSDat import GPSData
from ModuleDat import ModuleData


def main():
    main_module_data     = ModuleData()
    main_gps_data        = GPSData()
    main_api_logger      = APILog()
    main_sql_logger      = SQLog( filename    = 'test.db')
    global_reporter      = Report(sql_logger  = main_sql_logger,
                                  api_logger  = main_api_logger,
                                  gps_data    = main_gps_data,
                                  module_data = main_module_data)
    main_recorder        = Record(reporter    = global_reporter)
    global_reporter.report_all_unsent_data()
    main_recorder.start_record()
    global_reporter.start_status_updates()
    
    #global_reporter.stop_status_updates()
    #main_recorder.stop_record()
    
    
if __name__ == "__main__":main()