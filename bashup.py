#!/usr/bin/env python
# Simple 'game' with no real purpose
# by Siraj 'Sid' Rakhada sid-git@mindless.co.uk

# up/down to change speed
# left/right to change size
# space to change colour
# f to display FPS
# m to start/stop music - randomly
# p to pause
# IMPORTANT! ESC and l together to quit

import sys, pygame
import random
from pygame.locals import *
import math
import keyboard

#               R    G    B
WHITE       = (255, 255, 255)
GRAY        = (185, 185, 185)
BLACK       = (  0,   0,   0)
RED         = (155,   0,   0)
LIGHTRED    = (175,  20,  20)
GREEN       = (  0, 155,   0)
LIGHTGREEN  = ( 20, 175,  20)
BLUE        = (  0,   0, 155)
LIGHTBLUE   = ( 20,  20, 175)
YELLOW      = (155, 155,   0)
LIGHTYELLOW = (175, 175,  20)

BGCOLOR = BLACK
TEXTCOLOR = WHITE
TEXTSHADOWCOLOR = GRAY

TUNES = ['tetrisb.mid', 'tetrisc.mid']
BEEPLIST = ['beep1.ogg', 'beep2.ogg', 'beep3.ogg', 'beep4.ogg']

global direction, dirty_rects

direction=0 # store the direction of the rectangle travel, 0 = right, 1 = left

def main():
	global screen, WIDTH, HEIGHT, bgsurf, BIGFONT, BASICFONT, BEEPS
	global dirty_rects, oldText, dx, dy, speed, oldsize, clock
	oldText = None
	dirty_rects = []
	BEEPS = []
	displayFPS = 1
	fpscleared = 0
	playtime = 0
	speed = 100 # initial speed in pixels per second
	dx = dy = None

	oldsize = size = 200
	colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

	FPS=30

	# Block win/meta key
	keyboard.block_key('windows')

	pygame.init()
	#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
	screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	clock = pygame.time.Clock()        #create pygame clock object
	#pygame.display.set_caption('Hello World!')
	WIDTH=screen.get_width()
	HEIGHT=screen.get_height()
	BASICFONT = pygame.font.Font(None, 18)
	BIGFONT = pygame.font.Font(None, 100)
	#bgsurf = pygame.Surface(screen.get_size())
	#bgsurf = bgsurf.convert()
	#bgsurf.fill(BGCOLOR)
	screen.fill(BGCOLOR)
	pygame.key.set_repeat(500, 30)
	# load the sound files
	for i in range(len(BEEPLIST)):
		BEEPS.append(pygame.mixer.Sound(BEEPLIST[i]))

	curX = screen.get_size()[0]/2
	curY = screen.get_size()[1]/2


	playing = None
	screen.fill(BGCOLOR)
	pygame.display.flip()

	for i in range(len(BEEPS)):
		BEEPS[i].play()

	while True:
		milliseconds = clock.tick(FPS)
		seconds = milliseconds / 1000.0
		playtime += seconds
		keys = pygame.key.get_pressed()
		if keys[K_ESCAPE] and keys[K_l]:
			terminate()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == KEYDOWN:
				#if event.key == K_ESCAPE:
				#	terminate()
				if event.key == K_UP:
					if dx >= 0:
						speed += 10
						dx += 10
					else:
						speed -= 10
						dx -= 10
					if dy >= 0:
						dy += 10
					else:
						dy -= 10
				elif event.key == K_DOWN:
					if dx >= 0:
						dx -= 10
					else:
						dx += 10
					if dy >= 0:
						dy -= 10
					else:
						dy += 10
				elif event.key == K_RIGHT:
					size += 10
				elif event.key == K_LEFT:
					size -= 10
				elif event.key == K_SPACE:
					colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
				elif event.key == pygame.K_f:
					# clear the screen of the old fps text
					if displayFPS == 1 and oldText:
						oldText = None
						screen.fill(BGCOLOR)
						pygame.display.update()

					# toggle fps display
					displayFPS = not displayFPS
				elif event.key == pygame.K_m:
					if playing == None:
						pygame.mixer.music.load(TUNES[random.randint(0,len(TUNES)-1)])
						pygame.mixer.music.play(-1, 0.0)
						playing = True
					else:
						pygame.mixer.music.stop()
						playing = None
				elif event.key == pygame.K_p:
					# pause
					showTextScreen("PAUSED")
				else:
					rad = random.triangular(0,2*math.pi,1)
					dx = math.cos(rad)*abs(speed)
					dy = math.sin(rad)*abs(speed)

					sound = BEEPS[0]
					random.choice(BEEPS).play()



		if displayFPS and seconds % 1:
			# run FPS display code
			currentfps = "{:.2f}".format(clock.get_fps())
			displayFPStext(currentfps)


		(curX, curY)=moveRectangle(curX, curY, size, colour, seconds, speed)

		pygame.display.update(dirty_rects)
		#pygame.display.flip()
		dirty_rects = []

def terminate():
	pygame.quit()
	#print "dirty_rects at exit: ", len(dirty_rects)
	sys.exit()

def displayFPStext(fps):
	global oldText

	fpsfont = pygame.font.Font(None, 36)

	text = fpsfont.render(fps, 1, (0,0,255), BGCOLOR)
	newtextloc = text.get_rect(centerx=WIDTH/2)

	# no previous oldText, make one up
	if oldText == None:
		oldText = newtextloc

	# this draw over the old text
	pygame.draw.rect(screen, BGCOLOR, oldText)

	# this draws the new text
	screen.blit(text, newtextloc)

	# update the screen position where we just drew text and/or removed text
	dirty_rects.append(oldText.union(newtextloc))

	oldText = newtextloc

	return

def moveRectangle(x, y, size, colour, seconds, speed):
	global dx, dy, oldsize, BEEPS
	sound = None
	distance = HEIGHT
	if dx == None:
		dx = dy = speed # set initial speed - pixels per second
	if oldsize != size:
		# then we've had a size change
		rect = pygame.Rect(x, y, oldsize, oldsize)
		oldsize=size
		sound = BEEPS[0]
		sound.play()
	else:
		rect = pygame.Rect(x, y, size, size)

	pygame.draw.rect(screen, BGCOLOR, rect)
	dirty_rects.append(rect)


	x += dx * seconds # set distance of X movement per frame
	y += dy * seconds

	if x < 0:
		x = 0
		dx *= -1
		dx += random.randint(-15,15)
		sound = BEEPS[random.randint(0,len(BEEPS)-1)]
	elif x + size >= WIDTH:
		x = WIDTH - size
		dx *= -1
		dx += random.randint(-15,15)
		sound = BEEPS[random.randint(0,len(BEEPS)-1)]
	if y < 0:
		y = 0
		dy *= -1
		dy += random.randint(-15,15)
		sound = BEEPS[random.randint(0,len(BEEPS)-1)]
	elif y + size >= HEIGHT:
		y = HEIGHT - size
		dy *= -1
		dy += random.randint(-15,15)
		sound = BEEPS[random.randint(0,len(BEEPS)-1)]

	if sound != None:
		sound.play()

	rect = pygame.Rect(x, y, size, size)
	pygame.draw.rect(screen, colour, rect)
	dirty_rects.append(rect)
	#print "dx:", dx, "dy:", dy, "x:", x, "y:", y

	return (x, y)

# taken from tetromino demo
def showTextScreen(text):
	# This function displays large text in the
	# center of the screen until a key is pressed.
	# Draw the text drop shadow
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTSHADOWCOLOR)
	titleRect.center = (int(WIDTH / 2), int(HEIGHT / 2))
	screen.blit(titleSurf, titleRect)

	# Draw the text
	titleSurf, titleRect = makeTextObjs(text, BIGFONT, TEXTCOLOR)
	titleRect.center = (int(WIDTH / 2) - 3, int(HEIGHT / 2) - 3)
	screen.blit(titleSurf, titleRect)

	# Draw the additional "Press a key to play." text.
	pressKeySurf, pressKeyRect = makeTextObjs('Press a key to play.', BASICFONT, TEXTCOLOR)
	pressKeyRect.center = (int(WIDTH / 2), int(HEIGHT / 2) + 100)
	screen.blit(pressKeySurf, pressKeyRect)

	while checkForKeyPress() == None:
		pygame.display.update()
		clock.tick()

	screen.fill(BGCOLOR)
	pygame.display.update()

def makeTextObjs(text, font, color):
	surf = font.render(text, True, color)
	return surf, surf.get_rect()

def checkForKeyPress():
    for event in pygame.event.get():
        if event.type == QUIT:      #event is quit
            terminate()
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:   #event is escape key
                terminate()
            else:
                return event.key   #key found return with it
    # no quit or key events in queue so return None
    return None

if __name__ == '__main__':
	main()
