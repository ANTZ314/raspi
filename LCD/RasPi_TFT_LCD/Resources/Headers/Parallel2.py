#!/usr/bin/env python
# File count.py
# http://www.bristolwatch.com/pport/index.htm
# By Lewis Loflin - lewis@bvu.net
# For use with pyparallel

import parallel
import time
p = parallel.Parallel()

# Count 0-255 binary on 8 LEDs 
for var in range(0,256):
    p.setData(var)
    print var
    time.sleep(.5) #delay 500 mSec.

p.setData(0x00) # turn LEDs off
    
print "Good by!"

exit 
