# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 15:28:58 2017

@author: Jean Louw
"""

from Report import Report
from Record import Record
from SQLog import SQLog
from APILog import APILog

def main():
    
    main_API_logger = APILog()
    main_SQL_logger = SQLog(filename = 'main_gs.db')
    global_reporter = Report(sqlogger = main_SQL_logger,
                             apilogger = main_API_logger,
                             )
    
    recorder = Record(reporter=global_reporter)
    recorder.start_record()
    

if __name__ == "__main__":main()