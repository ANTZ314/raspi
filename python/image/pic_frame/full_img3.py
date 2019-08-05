# -*- coding: utf-8 -*-
"""
Description:
"""

import pygame
import sys
import os

def main():
	cnt = 0															# new file counter
	file_path1 = "/home/pi/Pictures/pics"			# path for new images
	
	pygame.init()
	screen = pygame.display.set_mode((0, 0))
	clock = pygame.time.Clock()											# setup the clock
	
	## Check for directory, if not then create it ##
	directory = os.path.dirname(file_path1)								# check in images file path
	if not os.path.exists(directory):									# if directory doesn't exist
		print("File path doesn't exist!")								# Notify that directory was created
	else:
		try:
			while True:
				for file in os.listdir(file_path1):							# each file in that folder
					if file.endswith(".jpg"):								# only do if .jpg file
						pics = os.path.join(file_path1, file)
						# Display different image on each iteration
						try:
							image = pygame.image.load(pics)
							pygame.display.flip()   
							screen.fill((255,255,255))
							screen.blit(image,(0,0))
							clock.tick(0.2)
							
							# Get Mouse events
							pressed1, pressed2, pressed3 = pygame.mouse.get_pressed()
							# Check if the left mouse button was pressed.
							if pressed1:
								print("Exit!")
								sys.exit(0)
							# Quit pygame.
							for event in pygame.event.get():
								if event.type == pygame.QUIT:
									running = False
						
						except KeyboardInterrupt:
							print("Exit!")
							sys.exit(0)
		except KeyboardInterrupt:
			print("Exit!")
			sys.exit(0)

if __name__ == "__main__": main()
