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
            if stopped.wait(timeout=0):
                break
            chunk = q.get()
            vol = max(chunk)
            if vol >= self.MIN_VOLUME:
                # TODO: write to file
                print "O",
            else:
                print "-",
    
    
    def process(self, stopped, q):
        while True:
            if stopped.wait(timeout = 0):
                break
            print "I'm processing..."
            #time.sleep(300)                                                     # why sleep for 5min?
            time.sleep(30)
    
            
    def listen(self, stopped, q):
         
        while True:
            if stopped.wait(timeout=0):
                break
            try:
                print self.process_g
                for i in range(0, int(44100 / 1024 * 5)):                       # ~215
                    data_chunk = array('h', self.stream.read(self.CHUNK_SIZE))  # 'h' = signed short (int)
                    vol = max(data_chunk)                                       # get highest value in the Array
                    if(vol >= self.MIN_VOLUME and vol < 1000):                   # if higher than threshold?
                        print "Vol: {}".format(vol)                             # Audio Trigger indicator
                    else:
                        print ".",                                              # listening indicator
                q.put(array('h', self.stream.read(self.CHUNK_SIZE)))            #
            except Full:
                pass  # discard

def main():
    Audio = audio()                                                             # create class object
    
    stopped = threading.Event()
    q = Queue()

    listen_t = threading.Thread(target=Audio.listen, args=(stopped, q))
    listen_t.start()
    
    record_t = threading.Thread(target=Audio.record, args=(stopped, q))
    record_t.start()
    
    process_g = threading.Thread(target=Audio.process, args=(stopped, q))
    process_g.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()


if __name__ == '__main__':
    main()
