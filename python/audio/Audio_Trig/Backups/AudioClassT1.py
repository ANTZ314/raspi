# -*- coding: utf-8 -*-
"""
Created on Feb 3rd 10:08:20 2017
@author: Antony Smith
@description: Class of Audio Operators
"""
import pyaudio
import wave
  
class AudioClass:  
    
    CHUNK = 4096                         # Audio chunk size
    FORMAT = pyaudio.paInt16             # Standard audio format (no change)
    CHANNELS = 2                         # Default number of channels = 1
    RATE = 48000                         # Samson sample rate
    DEVICE = 0				         # Found with "Device1/2.py" - Changes!
    RECORD_SECONDS = 5                   # Max audio record time (fails on higher?)
    WAVE_OUTPUT_FILENAME = "AUDIO.wav"   # Output Filename
    
    p = pyaudio.PyAudio()                # Create PyAudio object
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    frames = []                          # defined globally for both functions -> pass?

    def __init__(self, **kwargs):
        print"Class init!!"
        #self.properties = kwargs             # does what?
    
    def message(self, string):
        print("Message: {0}\n".format(str(string)))
    
    ## Check all Input & Output device -> find 'Audio' deviec ##
    def find_device(self):
        #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
        for i in range (0,self.numdevices):
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                        print "*Input Device id ", i, " ->", self.p.get_device_info_by_host_api_device_index(0,i).get('name')
                        if 'Audio' in str(self.p.get_device_info_by_host_api_device_index(0,i).get('name')):                            
                            self.DEVICE = i
                            #print "AUDIO DEVICE NO: ", self.DEVICE
        
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                        print "Output Device id ", i, " -> IGNORE OUTPUT DDEVICES!"
        
        # Manually using the device index of Samson Microphone
        devinfo = self.p.get_device_info_by_index(self.DEVICE)
        print ('\nSelected device is {0}'.format(devinfo.get('name')))
        
        
        if self.p.is_format_supported(self.RATE, #44100.0,                            # Sample rate
                                 input_device=devinfo["index"],             # 
                                 input_channels=devinfo['maxInputChannels'],# 
                                 input_format=pyaudio.paInt16):             # 
                                     print ('Supported Device Info:\nDevice Number: {0}\nWith Channels: {1}'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
        
        #print("\nTerminating...")
        #p.terminate()                                                      # terminate the input device here
        return devinfo
    
    ## Record data from default input device ##
    def getAudio(self, devinfo1):
        #print("\nGet Audio from Device: {0}".format(str(devinfo1["index"])))
        self.stream = self.p.open(format=self.FORMAT,
                    channels=devinfo1['maxInputChannels'],      # self.CHANNELS,
                    rate=self.RATE,                             # Mic rate 44100/48000
                    input_device_index=devinfo1["index"],       # self.DEVICE,
                    input=True,
                    frames_per_buffer=self.CHUNK)               # Chunk size causes 'Overflow'
                    
        print("* recording on Device: {0}".format(str(devinfo1["index"])))
        
        #frames = []                # now global
    
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
        
        print("* done recording")
        
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return
    
    ## Create the .wav file from previous recorded data ##
    def makeFile(self):
        print("* create & save Audio file!")
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close() 
        print ("File created succesfully")
        return
