#!/usr/bin/python
#
# An attempt to use a rotary encoder connected to BCM23 and BCM24 of a raspberry pi

import RPi.GPIO as GPIO
import time

encoderU = 4		# BCM no. of Encoder Up
encoderD = 3		# BCM no. of Encoder Down
encoderS = 2		# BCM no. of Switch

GPIO.setmode(GPIO.BCM)
GPIO.setup(encoderU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderS, GPIO.IN, pull_up_down=GPIO.PUD_UP)

count = 0
stateU = 0
stateD = 0
stateS = 0
countS = 0

def edgeU(channel):
	global count
	count = count + 1
	print "+", count

def edgeD(channel):
	global count
	count = count - 1
	print "-", count

#GPIO.add_event_detect(encoderU, GPIO.RISING, callback=edgeU)
#GPIO.add_event_detect(encoderD, GPIO.RISING, callback=edgeD)

try:
	while 1:
		time.sleep(0.001)
		s = GPIO.input(encoderU)
		if ( s != stateU ):
			stateU = s
			if ( s ):
				count = count + 1
				print "+", count
		s = GPIO.input(encoderD)
		if ( s != stateD ):
			stateD = s
			if ( s ):
				count = count - 1
				print "-", count
		s = GPIO.input(encoderS)
		if ( s ):
			if ( s == stateS ):
				if ( countS < 250 ):
					countS = countS + 1
					if ( countS == 250 ):
						print "L", count
			else:
				stateS = s
				countS = 1
		else:
			if ( s != stateS and countS < 250 ):
				print "S", count
			stateS = s
			countS = 0


# If CTRL+C is pressed, exit cleanly:
except KeyboardInterrupt:
		GPIO.cleanup() # cleanup all GPIO
		print ""

