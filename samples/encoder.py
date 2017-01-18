#!/usr/bin/python
#
# An attempt to us a Panasonic rotary encoder connected to BCM23 and BCM24 of a raspberry pi

import RPi.GPIO as GPIO
import time

encoderA = 23		# BCM no. of Encoder 'A'
encoderB = 24		# BCM no. of Encoder 'B'

GPIO.setmode(GPIO.BCM)
GPIO.setup(encoderA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

stateB = False
scale = 2
count = 0
countRaw = 0
countMax = 10*scale-1
countMin = 0

def edgeA(channel):
		global countRaw
		global countMax
		global countMin
		global count
		global stateB
		stateA = GPIO.input(encoderA)
		if stateA == stateB:
				countRaw = countRaw+1
		else:
				countRaw = countRaw-1
		if countRaw < countMin:
				countRaw = countMax
		if countRaw > countMax:
				countRaw = countMin
		countX = countRaw/scale
		if countX != count:
				count = countX
				print count

def edgeB(channel):
		global stateB
		stateB = GPIO.input(encoderB)

GPIO.add_event_detect(encoderA, GPIO.BOTH, callback=edgeA, bouncetime=10)
GPIO.add_event_detect(encoderB, GPIO.BOTH, callback=edgeB, bouncetime=10)

try:
		while 1:
				time.sleep(10)
# If CTRL+C is pressed, exit cleanly:
except KeyboardInterrupt:
		GPIO.cleanup() # cleanup all GPIO
		print ""

