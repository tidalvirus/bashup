#!/usr/bin/env python
# Simple background colour changing program
# Slooooooow
# by Siraj 'Sid' Rakhada sid-git@mindless.co.uk

import random, sys, time, pygame
from pygame.locals import *

FPS = 30
WINDOWWIDTH = 0
WINDOWHEIGHT = 0


#                R    G    B
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
BRIGHTRED    = (255,   0,   0)
RED          = (155,   0,   0)
BRIGHTGREEN  = (  0, 255,   0)
GREEN        = (  0, 155,   0)
BRIGHTBLUE   = (  0,   0, 255)
BLUE         = (  0,   0, 155)
BRIGHTYELLOW = (255, 255,   0)
YELLOW       = (155, 155,   0)
DARKGRAY     = ( 40,  40,  40)
bgColor = BLACK

def main():
	global FPSCLOCK, DISPLAYSURF, BASICFONT

	pygame.init()
	FPSCLOCK = pygame.time.Clock()
	#DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
	DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),pygame.FULLSCREEN)
	pygame.display.set_caption('norbash')

	BASICFONT = pygame.font.Font('freesansbold.ttf', 72)
	infoSurf = BASICFONT.render('BASH KEYS', 1, YELLOW)
	infoRect = infoSurf.get_rect()
	infoRect.topleft = (10, 25)

	while True:
		DISPLAYSURF.fill(bgColor)

		DISPLAYSURF.blit(infoSurf, infoRect)

		checkForQuit()
		for event in pygame.event.get():
			if event.type == KEYDOWN:
				changeBackgroundAnimation()
				DISPLAYSURF.fill(bgColor)

		pygame.display.flip()
		#pygame.time.wait(1000)

def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back

def changeBackgroundAnimation(animationSpeed=30):
    global bgColor
    newBgColor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    newBgSurf = pygame.Surface((WINDOWWIDTH, WINDOWHEIGHT))
    newBgSurf = newBgSurf.convert_alpha()
    oldr, oldg, oldb = bgColor
    r, g, b = newBgColor
    for alpha in range(0, 255, animationSpeed): # animation loop
        checkForQuit()

        newBgSurf.fill((r, g, b, alpha))
        DISPLAYSURF.blit(newBgSurf, (0, 0))

        pygame.display.flip()
        FPSCLOCK.tick(FPS)
    bgColor = newBgColor

if __name__ == '__main__':
    main()

