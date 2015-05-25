#!/usr/bin/env python
# Simple 'game' with no real purpose
# by Siraj 'Sid' Rakhada sid-git@mindless.co.uk

# up/down to change speed
# left/right to change size
# space to change colour
# f to display FPS
# IMPORTANT! ESC and p together to quit

import sys, pygame
import random
from pygame.locals import *

black = 0, 0, 0
background = black

global direction, dirty_rects

direction=0 # store the direction of the rectangle travel, 0 = right, 1 = left

def main():
	global screen, WIDTH, HEIGHT, bgsurf
	global dirty_rects, oldText, dx, dy, speed, oldsize
	oldText = None
	dirty_rects = []
	displayFPS = 1
	fpscleared = 0
	playtime = 0
	speed = 100 # initial speed in pixels per second
	dx = dy = None

	oldsize = size = 200
	colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

	FPS=30

	pygame.init()
	#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN|pygame.HWSURFACE|pygame.DOUBLEBUF)
	screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
	clock = pygame.time.Clock()        #create pygame clock object
	#pygame.display.set_caption('Hello World!')
	WIDTH=screen.get_width()
	HEIGHT=screen.get_height()
	bgsurf = pygame.Surface(screen.get_size())
	bgsurf = bgsurf.convert()
	bgsurf.fill(background)
	pygame.key.set_repeat(500, 30)

	curX = curY = 0

	screen.fill(black)
	pygame.display.flip()
	while True:
		milliseconds = clock.tick(FPS)
		seconds = milliseconds / 1000.0
		playtime += seconds
		keys = pygame.key.get_pressed()
		if keys[K_ESCAPE] and keys[K_p]:
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
						dx += 10
					else:
						dx -= 10
					if dy >= 0:
						dy += 10
					else:
						dy -= 10
				if event.key == K_DOWN:
					if dx >= 0:
						dx -= 10
					else:
						dx += 10
					if dy >= 0:
						dy -= 10
					else:
						dy += 10
				if event.key == K_RIGHT:
					size += 10
				if event.key == K_LEFT:
					size -= 10
				if event.key == K_SPACE:
					colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
				if event.key == pygame.K_f:
					# toggle fps display
					displayFPS = not displayFPS
					if fpscleared == 0:
						pygame.draw.rect(screen, background, pygame.Rect(oldText))
						fpscleared = 1
					if fpscleared == 1 and displayFPS == 1:
						fpscleared = 0

		if displayFPS and seconds % 1:
			# run FPS display code
			currentfps = "{:.2f}".format(clock.get_fps())
			displayFPStext(currentfps)
			#print clock.get_fps()

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
	text = fpsfont.render(fps, 1, (0,0,255), background)
	if oldText == None:
		oldText = text.get_rect(centerx=WIDTH/2)
	textrect = pygame.Rect(oldText)
	pygame.draw.rect(screen, background, textrect)
	dirty_rects.append(textrect)

	textrect = text.get_rect(centerx=WIDTH/2)
	dirty_rects.append(textrect)
	screen.blit(text, textrect)
	oldText=textrect
	#print textrect
	return

def moveRectangle(x, y, size, colour, seconds, speed):
	global dx, dy, oldsize
	distance = HEIGHT
	if dx == None:
		dx = dy = speed # set initial speed - pixels per second
	if oldsize != size:
		# then we've had a size change
		rect = pygame.Rect(x, y, oldsize, oldsize)
		oldsize=size
	else:
		rect = pygame.Rect(x, y, size, size)

	pygame.draw.rect(screen, background, rect)
	dirty_rects.append(rect)


	x += dx * seconds # set distance of X movement per frame
	y += dy * seconds

	if x < 0:
		x = 0
		dx *= -1
		dx += random.randint(-15,15)
	elif x + size >= WIDTH:
		x = WIDTH - size
		dx *= -1
		dx += random.randint(-15,15)
	if y < 0:
		y = 0
		dy *= -1
		dy += random.randint(-15,15)
	elif y + size >= HEIGHT:
		y = HEIGHT - size
		dy *= -1
		dy += random.randint(-15,15)

	rect = pygame.Rect(x, y, size, size)
	pygame.draw.rect(screen, colour, rect)
	dirty_rects.append(rect)
	#print "dx:", dx, "dy:", dy, "x:", x, "y:", y

	return (x, y)


if __name__ == '__main__':
	main()
