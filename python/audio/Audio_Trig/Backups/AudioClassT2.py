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
import wave
import sys
  
class AudioClass:  
    
    FORMAT = pyaudio.paInt16                # Default unchanged
    Threshold = 10                          # Energy threshold upper from 30 dB
    CHUNK = 4096                            # Audio chunk size 2**12 (default 1024)
    CHANNELS = 2                            # Will change to device's default
    RATE = 48000                            # Samson sample rate
    DEVICE = 0				            # Found with "Device1/2.py" - Changes!
    
    RECORD_SECONDS = 5                      # Max audio record time (fails on higher?)
    WAVE_OUTPUT_FILENAME = "AUDIO_T.wav"    # Output Filename
    SHORT_NORMALIZE = (1.0/32768.0)         # What is this for?
    swidth = 2                              # 
    Max_Seconds = 10                        # Time-out length
    TimeoutSignal=((RATE / CHUNK * Max_Seconds) + 2) # 2.46875 ?
    silence = True                          # 
    Time=0                                  # 
    all =[]                                 # 
    frames = []                             # defined globally for both functions -> pass?

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
        print("Message: {0}\n".format(str(string)))
    
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
            
            if self.p.is_format_supported(self.RATE, #44100.0,                            # Sample rate
                                     input_device=devinfo["index"],             # 
                                     input_channels=devinfo['maxInputChannels'],# 
                                     input_format=self.FORMAT):             # 
                                         print ('\nSupported Device Info:\nDevice: {0}\nChannels: {1}'.format(str(devinfo["index"]),str(devinfo['maxInputChannels'])))
        else:
            print "\nNo Audio device found... Exit for now"
            sys.exit()
        return devinfo      # return all of the Audio Devices specifications

###############################################################################

    def GetStream(self, CHUNK):
        return self.stream.read(CHUNK)

    def rms(self, frame):
            count = len(frame)/self.swidth
            format = "%dh"%(count)
            shorts = struct.unpack( format, frame )
    
            sum_squares = 0.0
            for sample in shorts:
                n = sample * self.SHORT_NORMALIZE
                sum_squares += n*n
            rms = math.pow(sum_squares/count,0.5)       # had a ';' ?
    
            return rms * 1000

    def WriteSpeech(self, WriteData):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(WriteData)
        wf.close()

    def KeepRecord(self, TimeoutSignal, LastBlock):
    
        all.append(LastBlock)
        for i in range(0, TimeoutSignal):
            try:
                self.data = self.GetStream(self.CHUNK)
            except:
                continue
            # I chage here (new Ident)
            all.append(self.data)
    
        print "End record after timeout"
        self.data = ''.join(all)
        print "Write to File: {0}".format(self.WAVE_OUTPUT_FILENAME)
        self.WriteSpeech(self.data)
        #silence = True
        #Time=0
        #listen(silence,Time)
        print"END HERE!!"
        sys.exit()    
    
    def listen(self, silence, Time, devinfo):    
        count = 0                               # generic counter to display RMS
        item = "."                              # count indicator for RMS display
        #print "\nWaiting for Speech..."
        while silence:
            try:
                input = self.GetStream(self.CHUNK)
            except:
                continue
            self.rms_value = self.rms(input)    # Get the
            count += 1                          # counter to not show RMS too often
            print item,                         # show counter (comma prints full stop)
            
            # Print the RMS value
            if count == 25:
                print("{0}".format(self.rms_value))
                count = 0                   # restart counter
                
            
            if (self.rms_value > self.Threshold):
                print "RMS ABOVE! {0}".format(self.rms_value)
                #silence=False
                #LastBlock=input
                #print "I'm Recording...."
                #self.KeepRecord(self.TimeoutSignal, LastBlock)
                
            Time = Time + 1                 # Timeout counter
    
            if (Time > self.TimeoutSignal):
                print "Time Out: No Speech Detected"
                sys.exit()
    

