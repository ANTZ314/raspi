# -*- coding: utf-8 -*-
"""
Created on Wed Jan 04 20:36:00 2017
@author: Jean Louw
Description: Python2.7 - Record 2 audio clips 10sec apart using a volume threshold,
             RMS signal compared to pre-defined THRESHOLD value - outputs accordingly
             '.' < THRESHOLD    '!' > THRESHOLD
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
#import os                      # to open gif file

class Record():
     
     once = 0
     FORMAT = pyaudio.paInt16
     #CHUNK = 4096          # larger chunk size?
     #CHANNELS = 2          # Default = 1
     #DEVICE = 4			  # Must select USB input device [SAMSON Mic] automatically
     #RATE = 48000          # SAMSON Microphone, Default = 44100
     #THRESHOLD = 10        # The threshold intensity that defines silence (3200)
            				  # and noise signal (an int. lower than THRESHOLD is silence)

     CHUNK = 1024          # Default
     CHANNELS = 1          # Default = 1
     RATE = 44100          # SAMSON Microphone Default = 44100
     THRESHOLD = 1200      # The threshold intensity that defines silence (3200)
            				  # and noise signal (an int. lower than THRESHOLD is silence).

     SILENCE_LIMIT = 1     # Silence limit in seconds. The max ammount of seconds where
        					 # only silence is recorded. When this time passes the
					     # recording finishes and the file is delivered.

     PREV_AUDIO = 0.5      # Previous audio (in seconds) to prepend. When noise
					     # is detected, how much of previously recorded audio is
					     # prepended. This helps to prevent chopping the beggining
					     # of the phrase.
    
     def __init__(self, **kwargs):
         self.recording = False                                         # Recording loop flag
         self.q = Queue()                                               # Object for moving audio blocks?
         self.stopped = threading.Event()                               # Time-out Event handler?
         self.sqlock = threading.Lock()                                 # ?
         self.apilock = threading.Lock()                                # ?
         self.p = pyaudio.PyAudio()
         self.stream = self.p.open(  format=self.FORMAT,
                                     channels=self.CHANNELS,            # Devcie dependant
                                     rate=self.RATE,                    # Device dependant
                                     #input_device_index = self.DEVICE,  # Set device input
                                     input=True,
                                     frames_per_buffer=self.CHUNK)
     
     def recording_function(self):
         cur_data = ''
         while self.recording:
            if self.stopped.wait(timeout=0): break
            else: 
                cur_data = self.stream.read(self.CHUNK)                 # Get audio stream in CHUNK size blocks
                self.q.put((cur_data))                                  # 
                              
     def start_record(self):
         self.recording = True
         recording_function_thread = threading.Thread(target=self.recording_function)
         recording_function_thread.start()
         processing_function_thread = threading.Thread(target=self.processing_function)
         processing_function_thread.start()
         print("Recording Started")
         
     def stop_record(self):
         self.recording = False
         print("Recording Stopped")
                
     def processing_function(self):
         #counter = 0
         cur_data = ''
         rel = self.RATE/self.CHUNK
         slid_win = deque(maxlen=self.SILENCE_LIMIT * rel)
#        prev_audio = deque(maxlen=self.PREV_AUDIO * rel)
         while True:
             if self.stopped.wait(timeout=0):
                 break
             else:
                 cur_data = self.q.get()                                    # 
                 slid_win.append(math.sqrt(abs(audioop.avg(cur_data, 4))))  # 
                 if(sum([x > self.THRESHOLD for x in slid_win]) > 0):       # 
                     if self.once == 0:                                     # only print 1 '!' when triggerd
                         print("!", end='')                                 # indicate: RMS > Threshold
                         self.once = 1
                 else:
                     print(".", end='')                                     # RMS indicator
                     #if counter == 5:                                      # every 5 input calculations
                     #    print("{0}".format(self.rms_value))               # print RMS value
                     #    counter = 0                                       # restart counter
                     #counter += 1                                          # increment counter


def RecordClassTestCode():
    recorde = Record()		# Initialise
    recorde.start_record()	# START
    time.sleep(10)			# Delay 10sec
    recorde.stop_record()		# STOP
    time.sleep(5)			    # Delay 10sec
    recorde.start_record()	# START
    time.sleep(10)		    # Delay 10sec
    recorde.stop_record()		# STOP
    print ('FINISHED...')		# DONE

if __name__ == "__main__": RecordClassTestCode()
