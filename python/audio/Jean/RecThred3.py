# -*- coding: utf-8 -*-
"""
Created:     Wed Mar 29 13:23:38 2017
@author:     Jean Louw
Description: Using threading to parallel process audio input & record audio
             with audio trigger
"""

import threading
from array import array
from Queue import Queue, Full
import time
import pyaudio


class audio():
    CHUNK_SIZE = 1024
    RATE = 44100
    CHANNELS = 2
    FORMAT = pyaudio.paInt16
    MIN_VOLUME = 350
    # if the recording thread can't consume fast enough, the listener will start discarding
    BUF_MAX_SIZE = CHUNK_SIZE * 10
    
    process_g = 0 
    p = pyaudio.PyAudio()
    
    def __init__(self, **kwargs):
        self.stream = self.p.open(format = self.FORMAT,
                        channels = self.CHANNELS,
                        rate = self.RATE,
                        input=True,
                        frames_per_buffer = self.CHUNK_SIZE)
    
    def record(self, stopped, q):
        while True:
            if stopped.wait(timeout=0):                 # time-out (Xsec?)
                break
            chunk = q.get()
            vol = max(chunk)                            # vol = largest value of Stream?
            if vol >= self.MIN_VOLUME:                  # if vol larger than threshold
                # TODO: write to file
                print "->{}".format(vol),                 # record the current stream until time-out?
            else:
                print "-*-",                            # just store chunk to buffer1/2/3
        print "\nRecord Time-Out..!"
        
    
    def process(self, stopped, q):
        while True:
            if stopped.wait(timeout = 0):               # if time-out exit this loop
                break
            print "I'm processing..."
            time.sleep(30)                              # run this every 30sec
        print "Process Time-Out..!"
    
            
    def listen(self, stopped, q):
        while True:                                                             # stay in this thread indefinitely
            if stopped.wait(timeout=0):                                         # break out if timed-out
                break
            try:
                print self.process_g
                for i in range(0, int(44100 / 1024 * 5)):                       # ~215
                    data_chunk = array('h', self.stream.read(self.CHUNK_SIZE))  # 'h' = signed short (int)
                    vol = max(data_chunk)                                       # get highest value in the Array
                    if(vol >= self.MIN_VOLUME and vol < 1000):                  # if higher than threshold?
                        print "Vol: {}".format(vol)                             # Audio Trigger indicator
                    else:
                        print ".",                                              # listening indicator
                q.put(array('h', self.stream.read(self.CHUNK_SIZE)))            # 
            except Full:
                pass  # Start discarding if Queue is full

def main():
    Audio = audio()                                                             # create class object
    
    stopped = threading.Event()                                                 # create thread stopper
    q = Queue()                                                                 # Queue object

    listen_t = threading.Thread(target=Audio.listen, args=(stopped, q))
    listen_t.start()
    
    record_t = threading.Thread(target=Audio.record, args=(stopped, q))
    record_t.start()
    
    process_g = threading.Thread(target=Audio.process, args=(stopped, q))
    process_g.start()

    try:
        while True:
            listen_t.join(0.1)      # Wait for thread to complete within 0.1sec
            record_t.join(0.1)      # Wait for thread to complete within 0.1sec
    except KeyboardInterrupt:       # [Ctrl+C] manual interrupt?
        stopped.set()               # Cause thread stop

    listen_t.join()                 # Wait for thread to complete
    record_t.join()                 # Wait for thread to complete
    
    print "* OVER & OUT *"

if __name__ == '__main__':
    main()
