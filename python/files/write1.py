# -*- coding: utf-8 -*-
"""
Python 2.7 (virtual env)
If file doesn't exist, file is created
If exists, opens existing file reads & prints contents
Appends 10 new lines
"""

import sys

def main():
	exists = 0											# append after printing contents
	try:												# Skip if file doesn't exist
		file = open('test.txt', 'r') 					# Open to read file
		print file.read()								# Print the contents
		file.close()									# Close the file
	except:
		exists = 1										# Don't append twice if file exists
		file= open("test.txt","a+")						# Create/open file then Append data 
		for i in range(10):								# 
			file.write("This is line %d\r\n" % (i+1))	# 
		file.close()									# Exit the opened file

	if exists == 0:										# append after printing contents
		file= open("test.txt","a+")						# Create/open file then Append data 
		for i in range(10):								# 
			file.write("This is line2 %d\r\n" % (i+1))	# 
		file.close()									# Exit the opened file
	else:												# 
		print "\nFile Didn't exist..."					# notification		
	
if __name__ == "__main__": main()
