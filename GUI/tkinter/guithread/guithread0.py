# -*- coding: utf-8 -*-
"""
Description: 
Tkinter & threading example??

Run:
python3 thread.py
"""
from Tkinter import *
from urllib2 import *
  
master = Tk()
  
def fetch_action():
    l.configure(text = "Beginning download")
    l.after(0, download)
  
def download():
    global total_read
    global stop_reading
  
    URL = "http://wiki.python.org/moin/RecentChanges"
    f = urlopen(URL)
    total_read = 0
    stop_reading = 0
    l.after(0, read_more, f, 100)
  
def read_more(handle, octets):
    global total_read
    global stop_reading
  
    if stop_reading:
        return
    print handle.read(octets),
    total_read += octets
    l.configure(text = "%d octets read" % total_read)
    l.after(1, read_more, handle, octets)
  
def stop():
    global stop_reading
  
    stop_reading = 1
  
l = Label(master, text = 40 * " ")
b1 = Button(master, text = "Fetch", command = fetch_action)
b2 = Button(master, text = "Stop reading", command = stop)
l.pack()
b1.pack()
b2.pack()
  
mainloop()
