# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 13:23:38 2017

@author: Jean Louw
"""

import threading
from array import array
from Queue import Queue, Full

import pyaudio


CHUNK_SIZE = 1024
MIN_VOLUME = 500
# if the recording thread can't consume fast enough, the listener will start discarding
BUF_MAX_SIZE = CHUNK_SIZE * 10


process_g = 0 

def main():
    stopped = threading.Event()
    q = Queue()

    listen_t = threading.Thread(target=listen, args=(stopped, q))
    listen_t.start()
    
    record_t = threading.Thread(target=record, args=(stopped, q))
    record_t.start()
    
    process_g = threading.Thread(target=process, args=(stopped, q))
    process_g.start()

    try:
        while True:
            listen_t.join(0.1)
            record_t.join(0.1)
    except KeyboardInterrupt:
        stopped.set()

    listen_t.join()
    record_t.join()


def record(stopped, q):
    while True:
        if stopped.wait(timeout=0):
            break
        chunk = q.get()
        vol = max(chunk)
        if vol >= MIN_VOLUME:
            # TODO: write to file
            print "O",
        else:
            print "-",


def process(stopped, q):
    while True:
        if stopped.wait(timeout = 0):
            break
        print "I'm processing.."
        time.sleep(300)

        
        
def listen(stopped, q):
    stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=2,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )

    while True:
        if stopped.wait(timeout=0):
            break
        try:
            print process_g
            for i in range(0, int(44100 / 1024 * 5)):
                data_chunk = array('h', stream.read(CHUNK_SIZE))
                vol = max(data_chunk)
                if(vol >= MIN_VOLUME):
                    print "WORDS.."
                else:
                    print "Nothing.."
            q.put(array('h', stream.read(CHUNK_SIZE)))
        except Full:
            pass  # discard


if __name__ == '__main__':
    main()