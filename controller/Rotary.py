#!/usr/bin/python
#
# Rotary dial control
#
# The hardware has 3 outputs. Two deliver pulses for roation (clockwise and anticlockwise)
# and the third gives the state of the pressbutton.
#
# Events generated:
# 	Rotate clockwise:		R+
#	Rotate anticlockwise:	R-
#	Short press:			Rs
#	Long press:				Rl
#
# (c) David Haworth

import RPi.GPIO as GPIO

encoderU = 4			# BCM no. of clockwise pulses
encoderD = 3			# BCM no. of anticlockwise pulses
encoderP = 2			# BCM no. of pressbutton
longPressTime = 0.5		# Duration of a long press

class Rotary:
	def __init__(self, eq, sleepyTime):
		self.eq = eq
		self.stateU = 0		# State of the up pulse input
		self.stateD = 0		# State of the down pulse input
		self.stateP = 0		# State of the press input
		self.countP = 0		# Counter for duration of press
		self.longPressTicks = longPressTime/sleepyTime
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(encoderU, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(encoderD, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		GPIO.setup(encoderP, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		return

	def Timer(self):					# Called infrequently to update status.
		return False

	def Poll(self):					# Called frequently to read input from rotary control.
		s = GPIO.input(encoderU)
		if ( s != self.stateU ):
			self.stateU = s
			if ( s ):
				self.eq.PutEvent("R+")

		s = GPIO.input(encoderD)
		if ( s != self.stateD ):
			self.stateD = s
			if ( s ):
				self.eq.PutEvent("R-")

		s = GPIO.input(encoderP)
		if ( s ):
			if ( s == self.stateP ):
				if ( self.countP < self.longPressTicks ):
					self.countP = self.countP + 1
					if ( self.countP >= self.longPressTicks ):
						self.eq.PutEvent("Rl")
			else:
				self.stateP = s
				self.countP = 1
		else:
			if ( s != self.stateP and self.countP < self.longPressTicks ):
				self.eq.PutEvent("Rs")
			self.stateP = s
			self.countP = 0

		return
