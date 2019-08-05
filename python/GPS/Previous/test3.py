# -*- coding: utf-8 -*-
"""
Trying to save each input character into string or list
"""
import sys
from time import sleep

def run():
	word1 = u'well look at that!'
	word2 = ['w','o','r','d','s',' ','a','n','d',' ','l','i','n','e','s']
	word3 = []
	
	#word1.encode('ascii')
	#word1.decode('utf-8')
	type(word1.encode('ascii'))
	print("{}".format(word1))
	
	print("{}".format(word2))
	str1 = ''.join(word2)
	print("{}".format(str(str1)))
	#word3 = word2
	#print("{}".format(word3))
	#del word2
	#print("{}".format(word3))
	#word2 = 'word2'
	#print("{}".format(word2))
	
if __name__ == '__main__': run()