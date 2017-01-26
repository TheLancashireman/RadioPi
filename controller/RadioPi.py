#!/usr/bin/python
#
# RadioPi.py - RadioPi main control program
#
# (c) David Haworth

from EventQueue import EventQueue
from MpdHandler import MpdHandler
from SysHandler import SysHandler
from UiHandler import UiHandler
from IrRc import IrRc
from Rotary import Rotary
from WebSock import WebSockHandler
import time

sleepyTime = 0.05	# Sleep time in seconds
longTime = 0.5		# Long time for timer events
longTicks = longTime/sleepyTime

eq = EventQueue()
mpdh = MpdHandler(eq)

source = [ IrRc(eq), Rotary(eq, sleepyTime), WebSockHandler(eq) ]
handler = [ mpdh, UiHandler(eq, mpdh), SysHandler(eq) ]

count = 0

while True:
	time.sleep(sleepyTime)

	# Poll all the event sources. Sources place their events in the event queue.
	for s in source:
		s.Poll()

	# Handle all the events. This may result in more events being generated.
	e = eq.GetEvent()
	while ( e != "" ):
		handled = False
		print e		# Debug
		for h in handler:
			if not handled:
				handled = h.Event(e)
		e = eq.GetEvent()

	#
	count += 1
	if count >= longTicks:
		#print 'Timer event'
		for s in source:
			s.Timer()
		for h in handler:
			h.Timer()
		count = 0
