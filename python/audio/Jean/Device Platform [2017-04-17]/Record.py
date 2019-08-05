# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 20:36:00 2017
@author: Jean Louw
Description: Python2.7 - Record 25sec audio clip using a volume threshold activation?
			 Auto-stop with 1sec of silence and prepend 500ms of audio to clip?
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
import datetime

class Record():
    
     FORMAT = pyaudio.paInt16
     CHUNK = 1024 
     CHANNELS = 1
     RATE = 44100
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
         if (self.data.get("reporter", None)!=None):print("Report Class Already Initialized")
         else: 
             self.data["reporter"] = Report.Report()
             print("New Report Class Initialized")
         
         self.recording_function_thread = threading.Thread(target=self.recording_function)
         self.pre_processing_function_thread = threading.Thread(target=self.pre_processing_function)
         self.processing_function_thread = threading.Thread(target=self.processing_function)
         #self.error_function_thread = threading.Thread(target=self.processing_function)
         
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
     
     
     def reset_threshold(self, num_samples = 50):
         values = [math.sqrt(abs(audioop.avg(self.stream.read(self.CHUNK), 4))) 
              for x in range(num_samples)] 
         values = sorted(values, reverse=True)
         r = sum(values[:int(num_samples * 0.1)]) / int(num_samples * 0.1)
         print (" Finished ")
         print (" Average audio intensity is {}".format(r))
         return r
         
     def recording_function(self):
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
         print("Recording Started")
         
     def stop_record(self):
         #self.recording_function_thread.stop()
         #self.pre_processing_function_thread.stop()
         #self.processing_function_thread.stop()
         
         self.stopped.set()
         self.recording = False
         print("Recording Stopped")
         
     ## After recorded this is data sent to API ##      
     def processing_function(self):
         while True:
             cur_data = self.processing_q.get()
             #ACTUAL PROCESSING INTERFACING | TYRON
             print("Sending " + str(self.processing_q.qsize()) + ": ", end='') 
             gunshot_event_data = {
                                  'dts':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"),
                                  'shots_fired' : 3,
                                  'screams':'unending'
                                  }
             record_data = {
                           'chunk': cur_data,
                           'gunshot_event': gunshot_event_data,     
                           }
             new_log_thread = threading.Thread(target=self.data['reporter'].report_live_event, args=(record_data,))
             new_log_thread.start()
             
             print("Threading count at {}".format(threading.active_count()))
             
             #self.stop_record()
         
             
     def pre_processing_function(self):
         cur_data = ''
         rel = self.RATE/self.CHUNK
         slid_win = deque(maxlen=(self.SILENCE_LIMIT * rel))
         audio2send = ''
         #slid_win.append(self.THRESHOLD)
         prev_audio = ''
         started = False
         
         while True:
             
            cur_data = self.pre_processing_q.get()
            
            slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))
            #print ('s-'+str(slid_win[-1]))
            if(sum([x > self.THRESHOLD for x in slid_win]) > 0):
                if(not started):
                    print ("Starting record of phrase")
                    started = True
                audio2send+=cur_data
            elif (started is True):
                print ("Finished")
                self.processing_q.put(prev_audio+audio2send)
                started = False
                slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
                prev_audio = '' 
                audio2send = ''
            else:
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
