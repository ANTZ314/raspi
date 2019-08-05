# -*- coding: utf-8 -*-

import sys
from time import sleep

list = ["$PUBX,40,GGA,0,0,0,0*5A",
		"$PUBX,40,GLL,0,0,0,0*5C",
		"this",
		"shit"]

def run():
	choice = 'z'
	for dick in list:
		vag = dick
		print("{}".format(vag))

	while choice != 'q':
		choice = raw_input("")
		if choice == 'a':
			#sys.exit(0)
			print('a'),
		else:
			print("*"),
	print('exit!!')
	sys.exit(0)
		
if __name__ == '__main__': run()