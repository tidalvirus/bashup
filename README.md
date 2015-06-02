# bashup
Simple Python Key Bashing Program

Important - starts up in full screen, and needs you to press ESC AND p together to quit.
This is so it can't be exited by accident.

## What does it do?

* Bounces a square on the screen off the edges. Colour can be changed, as can size and speed. Beeps (randomly) when the box hits the edge.
* Plays music (midi files from a pygame tetromino example)

## Commands

* F - toggle FPS (frames per second) display
* left/right arrow - change size of the square
* up/down arrow - change speed of the square
* M - toggle playing music - random tracks
* P - 'Pause' the game
* space bar - the square changes colour

## Requirements

This was written to run on a Raspberry Pi. It needs:

Python.
pygame.

That should be it.

## What will it do?

Hopefully, when I get time:

* Fade between colours.
* Leave a limited trail - configurable to be longer or shorter.
* Display more details - speed, FPS, directions, etc.
* Make a sound when it hits the edge - done 20150602.
* Display pictures instead of a square - change the picture on each bounce,
or press of the space bar instead of colours.
* Add more bouncing items on screen.

## Issues

* Beep is delayed from when the box hits the edge!
I've got no idea why, but on a Pi, the sound comes up later than when testing
the same thing on an old MacBook Air - which sometimes can't do the same speed
of graphics that the Pi can!

## The code is awful!

This is my first python program, which I've cobbled together from a few examples.
I know lots of things will need to change to accomodate the features I want to add.

## This is boring!

Well, it's just a pet project for me to make a 'game' for my toddler, that can't easily be escaped out
of, and can just be left running on a Pi.
