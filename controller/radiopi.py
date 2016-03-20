#!/usr/bin/python
#
# Headless control program for RadioPi

import RPi.GPIO as GPIO
import time
from mpd import MPDClient

# Initialise the MPD client
mpdc = MPDClient()
mpdc.timeout = 10
mpdc.idletimeout = None
mpdc.connect("localhost", 6600)

mpdstatus = mpdc.status()
volume = int(mpdstatus['volume'])

# Initialise GPIO for the rotary encoder
encoderA = 23       # BCM no. of Encoder 'A'
encoderB = 24       # BCM no. of Encoder 'B'

GPIO.setmode(GPIO.BCM)
GPIO.setup(encoderA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

stateB = False
countRaw = 0
countMax = 10*scale-1
countMin = 0

# Initialise controller state
modeVol = 1
mode = modeVol

# Callback for edge on channel A
def edgeA(channel):
	global countRaw
	global countMax
	global countMin
	global stateB
	stateA = GPIO.input(encoderA)
	if stateA == stateB:
		# Increase
		inc = 1
		if mode == modeVol
			if volume < 100
				volume += 1
				mpdc.setvol(str(volume))
	else:
		# Decrease
		inc = -1
		if mode == modeVol
			if volume > 0
				volume -= 1
				mpdc.setvol(str(volume))
	countRaw += inc
	if countRaw < countMin:
		countRaw = countMax
	if countRaw > countMax:
		countRaw = countMin

# Callback for edge on channel B
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
