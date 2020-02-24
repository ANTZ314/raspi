#!/bin/bash

# Make executable:
#chmod u+x hello-world

#Copy file from Pi:
#scp pi@192.168.8.101:/home/pi/test.jpg /home/antz/Desktop/

#Copy file to Pi:
#scp /home/antz/Desktop/gui1.py pi@192.168.8.101:/home/pi/Documents/

#Copy folder to Pi:
#scp -r /home/antz/Desktop/omnicode pi@192.168.8.100:/home/pi/Documents/

#Copy folder from Pi:
scp -r pi@192.168.8.100:/home/pi/omnicode /home/antz/Desktop/