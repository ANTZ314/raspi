# -*- coding: utf-8 -*-
"""
Checking input devices for the SAMSON then use that device[index] for recording function
"""
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000                 # Sample rate
DEVICE = 4				  # Found with "Device1/2.py"
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "AUDIO5.wav"

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')
frames = []                 # defined globally for both functions -> pass?

def find_device():
    #for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
    for i in range (0,numdevices):
            if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                    print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
    
            if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                    print ("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))
    
    devinfo = p.get_device_info_by_index(DEVICE)
    print ("Selected device is ",devinfo.get('name'))
    
    
    if p.is_format_supported(RATE,      #44100.0,  # Sample rate
                             input_device=devinfo["index"],
                             input_channels=devinfo['maxInputChannels'],
                             input_format=pyaudio.paInt16):
                                 print ('Device Supported...')
    
    #print("\nTerminating...")
    #p.terminate()

# Record data from default input device
def getAudio():
    stream = p.open(format=FORMAT,
                channels=CHANNELS,              # devinfo['maxInputChannels'],
                rate=RATE,
                input_device_index = DEVICE,    # devinfo["index"],
                input=True,
                frames_per_buffer=CHUNK)
                
    print("* start recording")
    
    #frames = []                # now global

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    
    print("* done recording")
    
    stream.stop_stream()
    stream.close()
    p.terminate()

# Create the .wav file from previous recorded data
def makeFile():
    print ("* creating file named: {0}".format(WAVE_OUTPUT_FILENAME))
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == "__main__":
    find_device()
    getAudio()
    makeFile()
    print("Complete...")
    
