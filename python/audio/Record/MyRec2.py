"""
Created on Wed Mar 15 11:32:43 2017
@author: antz
"""
import pyaudio
import wave

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
DEVICE = 4
RECORD_SECONDS = 10
WAVE_OUTPUT_FILENAME = "record2.wav"

p = pyaudio.PyAudio()
frames = []             # defined globally for both functions -> pass?

# Record data from default input device
def getAudio():
    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                #input_device_index = DEVICE,
                input=True,
                frames_per_buffer=CHUNK)
                
    print("* recording")
    
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
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

getAudio()
makeFile()