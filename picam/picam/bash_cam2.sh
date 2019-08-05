#!/bin/bash

DATE=$(date +'%Y%m%d')

raspivid -o /home/pi/Documents/picam/$DATE.h264 -t 5000
