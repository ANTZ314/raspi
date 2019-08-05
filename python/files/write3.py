# -*- coding: utf-8 -*-
"""
Python 2.7 (virtual env)
-> If directory doesn't exist, it is created
-> If it exists, opens existing directory & prints contents
"""

import sys
import os

def main():
	exists = 0											# variable to append after printing contents
	cnt = 0												#
	file_path1 = "/home/antz/0Python/files/notes.txt"	#
	file_path2 = "/home/antz/0Python/image"				#

	directory = os.path.dirname(file_path1)
	if not os.path.exists(directory):
		os.makedirs(directory)
		print("Create Directory")
	else:
		print("Already Exists")
	
	for file in os.listdir(file_path2):
		print("{0}".format(os.listdir(file_path2)[cnt]))
		cnt += 1
	
	
if __name__ == "__main__": main()
