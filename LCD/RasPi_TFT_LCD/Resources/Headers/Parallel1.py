#!/usr/bin/env python
# File pportbits.py
# http://www.bristolwatch.com/pport/index.htm
# By Lewis Loflin - lewis@bvu.net
# Example code to turn ON-OFF individual bits on PC 
# printer port Db25 pins 2-9.
# Must use my version of pyparallel on website for p.data().
# Bitwise AND is used to clear a bit while bitwise OR used to set bit.

import parallel
p = parallel.Parallel()

def writeD0(bit_val):
    if bit_val == 1:
        p.setData(p.data() | 1) # set bit 0
    else: # clear bit 0
        p.setData(p.data() & (255 - 1))
    return

def writeD1(bit_val):
    if bit_val == 1:
        p.setData(p.data() | 2) #set bit 1
    else: # clear bit 1
        p.setData(p.data() & (255 - 2))
    return

def writeD2(bit_val):
    if bit_val == 1:
        p.setData(p.data() | 4) #set bit 2
    else: # clear bit 2
        p.setData(p.data() & (255 - 4))
    return

def writeD3(bit_val):
    if bit_val == 1:
        p.setData(p.data() | 8) #set bit 3
    else: # clear bit 3
        p.setData(p.data() & (255 - 8))
    return

def writeD4(bit_val):
    if bit_val == 1:
        p.setData(p.data() | 16) #set bit 4
    else: # clear bit 4
        p.setData(p.data() & (255 - 16))
    return

def writeD5(bit_val):
    if bit_val == 1:
        p.setData(p.data() | 32) #set bit 5
    else: # clear bit 5
        p.setData(p.data() & (255 - 32))
    return

def writeD6(bit_val):
    if bit_val == 1:
        p.setData(p.data() | 64) #set bit 6
    else: # clear bit 6
        p.setData(p.data() & (255 - 64))
    return

def writeD7(bit_val):
    if bit_val == 1:
        p.setData(p.data() | 128) #set bit 7
    else: # clear bit 7
        p.setData(p.data() & (255 - 128))
    return

# convert an 8-bit number (integer) to a binary. 
# Returns string.
# unlike python bin() this doesn't drop leading zeros
def convBinary(value):
    binaryValue = 'b'
    for  x in range(0, 8):
        temp = value & 0x80
        if temp == 0x80:
           binaryValue = binaryValue + '1'
        else:
            binaryValue = binaryValue + '0'
        value = value << 1
    return binaryValue
    

# Set all data port bits to 0
p.setData(0) # LEDs off
print "Port data latches =", p.data() 
# read port data latches - should be 0

# use differing combinations 

# set bits D0, D1, D7 
writeD0(1)
writeD1(1)
writeD7(1)

# Read and print data port:
xp = p.data()
print "Value of data port =", convBinary(xp), " ", hex(xp) 
# should be Value of data port = b10000011   0x83 
# LEDs connected to port will show 10000011  
print
print "Good by!"

exit
