# -*- coding: utf-8 -*-
"""
Trying to save each input character into string or list
"""
import sys
from time import sleep

words = 'qwerty,asdf'

def run():
	for i in range(1, 5):
		print(words[i])
	
if __name__ == '__main__': run()