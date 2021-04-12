#!/bin/bash

######################
## Make executable: ##
#chmod u+x hello-world

## Get Ip Address: ##
# hostname -I

##  Usage: ##
# cd ~/Desktop/temp/
# ./rpi.sh
######################

##########
# FROM PI:
##########

## FILE ##
#scp pi@192.168.0.114:/home/pi/eject.py /home/antz/Desktop/

## FOLDER ##
#scp -r pi@192.168.0.104:/home/pi/main3 /home/antz/Desktop/

##########
# TO PI:
##########

## FILE ##
#scp /home/antz/Desktop/temp/gait/readme.md pi@192.168.0.104:/home/pi/

## FOLDER ##
#scp -r /home/antz/Desktop/iot/main pi@192.168.1.110:/home/pi/


