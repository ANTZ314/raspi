# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 20:36:00 2017

@author: Jean Louw
"""
from __future__ import print_function
try:
    from queue import Queue
except:
    from Queue import Queue
import threading
import pyaudio
import time
import audioop
import math
from collections import deque
import Report

class Record():
    
     __version__ = "2017.1"
    
     FORMAT = pyaudio.paInt16
     CHUNK = 1024 
     CHANNELS = 1
     RATE = 44100
     ERROR_THRESHOLD = 100
     THRESHOLD = 3200  # The threshold intensity that defines silence
                  # and noise signal (an int. lower than THRESHOLD is silence).

     SILENCE_LIMIT = 1  # Silence limit in seconds. The max ammount of seconds where
                   # only silence is recorded. When this time passes the
                   # recording finishes and the file is delivered.

     PREV_AUDIO = 0.5  # Previous audio (in seconds) to prepend. When noise
                  # is detected, how much of previously recorded audio is
                  # prepended. This helps to prevent chopping the beggining
                  # of the phrase.
     
    
     def __init__(self, **kwargs):
         
         self.data = kwargs
         # Ensure that an instance of Report class is passed
         if (self.data.get("reporter", None)!=None):print("Report Class Already Initialized")
         else:
             print("No Report Class Initialized")
             raise StandardError("pass report class through calling Record(reporter = your_report_class_instance)")
             
         # Ensure that an instance of GPSDat class is passed
         if (self.data["reporter"].data.get("gps_data", None)!=None):
             print("GPSDat Class Already Initialized")
             self.data["gps_data"]=self.data["reporter"].data["gps_data"]
         else:
             print("No GPS Class Initialized")
             raise StandardError("pass gps source class through calling Record(gps_data = your_report_class_instance)")
             
         self.recording_function_thread = threading.Thread(target=self.recording_function)
         self.pre_processing_function_thread = threading.Thread(target=self.pre_processing_function)
         self.processing_function_thread = threading.Thread(target=self.processing_function)
         self.error_function_thread = threading.Thread(target=self.processing_function)
         self.error_state = False
         
         self.processing_q = Queue()
         self.pre_processing_q = Queue()
         
         self.recording = False
         self.stopped = threading.Event()
         
         self.sqlock = threading.Lock()
         self.apilock = threading.Lock()
         
         self.data["reporter"].set_locks(self.apilock, self.sqlock)
         
         self.pyaudio_obj = pyaudio.PyAudio()
         self.stream = self.pyaudio_obj.open(    
                                                 format=self.FORMAT,
                                                 channels=self.CHANNELS,
                                                 rate=self.RATE,
                                                 input=True,
                                                 frames_per_buffer=self.CHUNK 
                                             )
         
         self.THRESHOLD = self.reset_threshold(100)
     
     def error_capture_function(self):
         while True:
             while(not self.error_state): pass # waits for error
             error_data = {
                               'module_version':self.__version__,
                               'error_details':"Microphone not functioning properly"
                           }
             new_report_thread = threading.Thread(target=self.data['reporter'].report_error, args=(error_data,))
             self.data['reporter'].microphone_functional = False
             new_report_thread.start()
             while(self.error_state): pass # waits for error cleared
             self.data['reporter'].microphone_functional = True
                 
     def reset_threshold(self, num_samples = 50):
         #set minimum threshold
         values = [math.sqrt(abs(audioop.avg(self.stream.read(self.CHUNK), 4))) 
              for x in range(num_samples)] 
         values = sorted(values, reverse=True)
         r = sum(values[:int(num_samples * 0.1)]) / int(num_samples * 0.1)
         print (" Finished ")
         print (" Average audio intensity is {}".format(r))
         #also pass on the signal to noise ratio
         self.data['reporter'].microphone_snr = 'init_snr'
         return r
         
     def recording_function(self):
         #cur_data = ''
         while self.recording:
            if self.stopped.wait(timeout=0): break
            else: 
                cur_data = self.stream.read(self.CHUNK)
                self.pre_processing_q.put(cur_data)
                
     def start_record(self):
         self.pre_processing_q.empty()
         self.processing_q.empty()
         self.stopped.clear()
         self.recording = True
         
         self.recording_function_thread.start()
         self.pre_processing_function_thread.start()
         self.processing_function_thread.start()
         self.error_function_thread.start()
         print("Recording Started")
         
     def stop_record(self):
         #self.recording_function_thread.stop()
         #self.pre_processing_function_thread.stop()
         #self.processing_function_thread.stop()
         
         self.stopped.set()
         self.recording = False
         print("Recording Stopped")
                  
     def processing_function(self):
         while True:
             preprocess_data = self.processing_q.get()
             gunshot_event_data = {
                                  'start_time'  :preprocess_data['start_time'],
                                  'stop_time'   :preprocess_data['stop_time'],
                                  'shots_fired' : 3,
                                  }
             record_data = {
                           'chunk': preprocess_data['audio'],
                           'gunshot_event': gunshot_event_data,     
                           }
             new_report_thread = threading.Thread(target=self.data['reporter'].report_live_event, args=(record_data,))
             new_report_thread.start()
             #also update the signal to noise ratio
             self.data['reporter'].microphone_snr = 'upd_snr'
             
             print("Threading count at {}\n".format(threading.active_count()))
             
             #self.stop_record()
         
     def pre_processing_function(self):
         cur_data = ''
         rel = self.RATE/self.CHUNK
         slid_win = deque(maxlen=(self.SILENCE_LIMIT * rel))
         audio2send = ''
         #slid_win.append(self.THRESHOLD)
         prev_audio = ''
         started = False
         preprocess_data = {}
         while True:
            cur_data = self.pre_processing_q.get()
            
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            #print ('s-'+str(slid_win[-1]))
            if(sum([x > self.THRESHOLD for x in slid_win]) > 0):
                self.error_state = False
                if(not started):
                    preprocess_data['start_time'] = self.data['gps_data'].current_time
                    print ("Starting record of phrase")
                    started = True
                audio2send+=cur_data
            elif (started is True):
                print ("Finished")
                preprocess_data['stop_time'] = self.data['gps_data'].current_time
                preprocess_data['audio'] = prev_audio + audio2send
                self.processing_q.put(preprocess_data)
                started = False
                slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
                prev_audio = '' 
                audio2send = ''
            elif (sum([x > self.ERROR_THRESHOLD for x in slid_win]) == 0):
                self.error_state = True
            else:
                self.error_state = False
                prev_audio+=cur_data
            
            
                
def RecordClassTestCode():
    recorde = Record(module_id='KingPin',
                     module_longitude = 'long',
                     module_latitude  = 'lat')
    recorde.start_record()
    time.sleep(25)
    recorde.stop_record()
    #time.sleep(10)
    #recorde.start_record()
    #time.sleep(10)
    #recorde.stop_record()

if __name__ == "__main__": RecordClassTestCode()
