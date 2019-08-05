# -*- coding: utf-8 -*-
"""
Created on Mon May 15 10:10:58 2017

@author: Jean Louw
"""

# -------------------------------------------------------------------------#
# Name: imports.py                                                         #
# Function: This should be run before the rest of the code to ensure       #
#           that all modules and dependencies are installed.               #
# Dependencies: pip                                                        #
# -------------------------------------------------------------------------#

#-------------------------------------IMPORTS----------------------------------

try:
    import pyaudio
except:
    import pip
    pip.main(['install', 'pyaudio'])

try:
    import requests
except:
    import pip
    pip.main(['install', 'requests'])

try:
    import psutil
except:
    import pip
    pip.main(['install', 'psutil'])

try:
    import pyfirmata
except:
    import pip
    pip.main(['install','pyfirmata'])

#------------------------------------------------------------------------------