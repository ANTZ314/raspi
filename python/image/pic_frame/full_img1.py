# -*- coding: utf-8 -*-
"""
Description: Displays 2 images in full screen mode
			 Loops continuously [ctrl+C to exit]
"""

import pygame
import sys

def main():
	try:
		pygame.init()
		screen = pygame.display.set_mode((0, 0))
		done = False
		image1 = pygame.image.load("img1.jpg")
		image2 = pygame.image.load("img2.jpg")

		clock = pygame.time.Clock()

		while not done:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
			screen.fill((255,255,255))
			screen.blit(image1,(0,0))
			clock.tick(1)
			pygame.display.flip()   
			screen.fill((255,255,255))
			screen.blit(image2,(0,0))
			clock.tick(0.5)
			pygame.display.flip()
			clock.tick(0.5)
	except KeyboardInterrupt:
		print("Exit!")
		sys.exit(0)

if __name__ == "__main__": main()
