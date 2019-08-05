# -*- coding: utf-8 -*-
"""
Created on Feb 3rd 10:08:20 2017
@author: Antony Smith
@description: Class containing functions to find audio device, then initialise stream
              using that devices details, then wait for an audio trigger to start recording
              a predefined sound clip (10sec?) or stop when no audio recieved (time-out for both)
"""
import pyaudio
import math
import struct
#import wave
import sys
  
class AudioClass:  
    
    FORMAT = pyaudio.paInt16                # Default unchanged
    Threshold = 5                           # Energy threshold upper from 30 dB
    CHUNK = 4096                            # Audio chunk size 2**12 (default 1024)
    #CHUNK = 48000
    CHANNELS = 2                            # Will change to device's default
    RATE = 48000                            # Samson sample rate
    DEVICE = 0				            # Found with "Device1/2.py" - Changes!
    
    RECORD_SECONDS = 5                      # Max audio record time (fails on higher?)
    WAVE_OUTPUT_FILENAME = "AUDIO_T.wav"    # Output Filename
    SHORT_NORMALIZE = (1.0/32768.0)         # What is this for?
    swidth = 2                              # 
    Max_Seconds = 10                        # Time-out length
    TimeoutSignal=((RATE / CHUNK * Max_Seconds) + 2) # 2.46875 ?
    silence = True                          # ?
    Time=0                                  # ?
    all =[]                                 # ?
    frames = []                             # defined globally for both functions -> pass?

    """
    p = pyaudio.PyAudio()
    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')    
    stream = p.open(format = FORMAT,
                channels = CHANNELS,
                rate = RATE,
                input_device_index = DEVICE,
                input = True,
                output = True,
                frames_per_buffer = CHUNK)
    """

    def __init__(self, **kwargs):
        print("Stream init!!")
        self.p = pyaudio.PyAudio()
        self.info = self.p.get_host_api_info_by_index(0)
        self.numdevices = self.info.get('deviceCount')
        self.stream = self.p.open(format = self.FORMAT,
                channels = self.CHANNELS,
                rate = self.RATE,
                input_device_index = self.DEVICE,
                input = True,
                output = True,
                frames_per_buffer = self.CHUNK)
    
    def message(self, string):
        print("Warp Speed... {0}\n".format(str(string)))
    
    def find_device(self):
        Found = 0                           # Device found? (1 = Yes / 0 = No)
        #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
        for i in range (0,self.numdevices):
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                        print (" Input Device id {0} - {1}".format(i, self.p.get_device_info_by_host_api_device_index(0,i).get('name')))
                        if 'Audio' in str(self.p.get_device_info_by_host_api_device_index(0,i).get('name')):                            
                            Found = 1
                            self.DEVICE = i
        
                if self.p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                        print ("Output Device id {0} - {1}".format(i, self.p.get_device_info_by_host_api_device_index(0,i).get('name')))
        
        if Found == 1:
            # Manually using the device index of Samson Microphone
            devinfo = self.p.get_device_info_by_index(self.DEVICE)
            print ('Selected device is: {0}'.format(devinfo.get('name')))
            
            if self.p.is_format_supported(self.RATE,                            # Sample rate
                                     input_device=devinfo["index"],             # Which device to select
                                     input_channels=devinfo['maxInputChannels'],# Number of channels
                                     input_format=self.FORMAT):                 # Default
                                         print ('\nSupported Device -{0}- has -{1}- Channels\n'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
        else:
            print ("\nNo Audio device found... Exit for now")
            sys.exit()
        return devinfo      # return all of the Audio Devices specifications

###############################################################################

    def GetStream(self):
        return self.stream.read(self.CHUNK)
        

    def rms(self, frame):
            count = len(frame)/self.swidth
            format = "%dh"%(count)
            shorts = struct.unpack( format, frame )
    
            sum_squares = 0.0
            for sample in shorts:
                # sample is a signed short in +/- 32768. 
                # normalize it to 1.0
                n = sample * self.SHORT_NORMALIZE
                sum_squares += n*n
            rms = math.pow(sum_squares/count,0.5);
    
            return rms * 1000   
    
    def listen(self, silence, Time, devinfo):    
        counter = 0                             # generic counter to display RMS
        #item = "."                              # count indicator for RMS display
        #print ("\nWaiting for Speech...")
        while silence:
            try:
                input = self.GetStream()
            except:
                continue
            
            self.rms_value = self.rms(input)    # Get the average/normalised RMS value
            counter += 1                        # counter to not show RMS too often
            print (".", end=' ')                # print same line {python2.x - (item,)}
            
            # Print the RMS value
            if counter == 5:
                print("{0}".format(self.rms_value))
                counter = 0                     # restart counter
            
            if (self.rms_value > self.Threshold):
                print ("RMS ABOVE! {0}".format(self.rms_value))
                
            Time = Time + 1                 # Timeout counter
    
            if (Time > self.TimeoutSignal):
                print ("Time Out: No Speech Detected")
                sys.exit()
    

