# -*- coding: utf-8 -*-
"""
Python 2.7 (virtual env)
Opens existing file reads & prints contents then appends 10 new lines
"""
import sys

def main():
	file = open('test.txt', 'r') 
	print file.read()
	file.close()
	
	
	f= open("test.txt","a+")
	for i in range(10):
		 f.write("This is line2 %d\r\n" % (i+1))
	file.close()

if __name__ == "__main__": main()
