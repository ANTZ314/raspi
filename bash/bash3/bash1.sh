#!/bin/bash

DATE=$(date +'%Y-%m-%d_%H%M')

raspistill -o /home/pi/Documents/bash/bash3/pipics/$DATE.jpg
