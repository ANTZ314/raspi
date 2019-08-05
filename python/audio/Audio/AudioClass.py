# -*- coding: utf-8 -*-
"""
Created on Feb 3rd 10:08:20 2017
@author: Antony Smith
@description: Class of Audio Operators
"""
import pyaudio
import wave
  
class AudioClass:  
    
    CHUNK = 4096                         # Audio chunk size 2**12 (default 1024)
    FORMAT = pyaudio.paInt16             # 
    CHANNELS = 2                         # 
    RATE = 48000                         # Samson sample rate
    DEVICE = 0				         # Found with "Device1/2.py" - Changes!
    RECORD_SECONDS = 5                   # Max audio record time (fails on higher?)
    WAVE_OUTPUT_FILENAME = "AUDIO.wav"   # Output Filename
    
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    frames = []                         # defined globally for both functions -> pass?

    def __init__(self, **kwargs):
        print("Class init!!")
        #self.properties = kwargs             # does what?
    
    def message(self, string):
        print("Message: " + str(string), "\n")
    
    def find_device(self):
        #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
        for i in range (0,self.numdevices):
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                        print ("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0,i).get('name'))
                        if 'Audio' in str(self.p.get_device_info_by_host_api_device_index(0,i).get('name')):                            
                            self.DEVICE = i
                            print ("AUDIO DEVICE NUMBER: ", self.DEVICE)
        
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                        print ("Output Device id ", i, " -> IGNORE OUTPUT DDEVICES!")
        
        # Manually using the device index of Samson Microphone
        devinfo = self.p.get_device_info_by_index(self.DEVICE)
        print ("\nSelected device is ",devinfo.get('name'))
        
        
        if self.p.is_format_supported(self.RATE,                            # Sample rate
                                 input_device=devinfo["index"],             # Which device to select
                                 input_channels=devinfo['maxInputChannels'],# Number of channels
                                 input_format=pyaudio.paInt16):             # Default
                                     print ('Supported Device Info:')
                                     print ("Device number: ", str(devinfo["index"]))
                                     print ("Channels: ", str(devinfo['maxInputChannels']))
        
        #print("\nTerminating...")
        #p.terminate()
        return
    
    # Record data from default input device
    def getAudio(self):
        #print("\nGet Audio from Device: ", self.DEVICE)
        self.stream = self.p.open(format=self.FORMAT,
                    channels=self.CHANNELS,              # devinfo['maxInputChannels'],
                    rate=self.RATE,
                    input_device_index=self.DEVICE,      # devinfo["index"],
                    input=True,
                    frames_per_buffer=self.CHUNK)
                    
        print("* recording on Device: ", self.DEVICE)
        
        #frames = []                # now global
    
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
        
        print("* done recording...")
        
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        return
    
    # Create the .wav file from previous recorded data
    def makeFile(self):
        print("* create & save Audio file as: {0}".format(self.WAVE_OUTPUT_FILENAME))
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close() 
        print ("* file created succesfully\n")
        return