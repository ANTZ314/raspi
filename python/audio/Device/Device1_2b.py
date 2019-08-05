# -*- coding: utf-8 -*-
"""
Description:    Checks and displays all IO devices, then if Audio device number (index)
                is correct (line22) it will confirm if format is supported.

Also use "lsusb" to view plugged in devices - Tho device number is incorrect
"""
# cat d.py
import pyaudio

CHUNK = 1024					# 
FORMAT = pyaudio.paInt16			# 
CHANNELS = 1					# Number of channels
RATE = 48000.0                    	# Sammple rate
#RATE = 44100.0                      # Default sample rate
DEVICE = 4				     		# Found with "Device1/2.py"
RECORD_SECONDS = 5				# record time maximum?
WAVE_OUTPUT_FILENAME = "AUDIO.wav"	# Output file name

p = pyaudio.PyAudio()
info = p.get_host_api_info_by_index(0)
numdevices = info.get('deviceCount')

#for each audio device, determine if is an input or an output and add it to the appropriate list and dictionary
for i in range (0,numdevices):
        if p.get_device_info_by_host_api_device_index(0,i).get('maxInputChannels')>0:
                print ("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))

        if p.get_device_info_by_host_api_device_index(0,i).get('maxOutputChannels')>0:
                print ("Output Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0,i).get('name'))

# Must select the correct index number to pass "Support Test":
devinfo = p.get_device_info_by_index(DEVICE)
print ("Selected device is ",devinfo.get('name'))

# If parameters are correct for Audio device print "Supported"
if p.is_format_supported(RATE,  								# Sample rate
                         input_device=devinfo["index"],				# selected device
                         input_channels=devinfo['maxInputChannels'],       # Number of channels detected
                         input_format=pyaudio.paInt16):				# default
                             print ('\n* Device Supported...')			     # Print

p.terminate()
