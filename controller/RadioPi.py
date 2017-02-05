#!/usr/bin/python
#
# RadioPi.py - RadioPi main control program
#
# (c) David Haworth

from EventQueue import EventQueue
from MpdHandler import MpdHandler
from SysHandler import SysHandler
from NetHandler import NetHandler
from UiHandler import UiHandler
from IrRc import IrRc
from Lirc import Lirc
from Rotary import Rotary
from WebSock import WebSockHandler
from RadioPiLib import Dbg_Print
import time

sleepyTime = 0.005	# Sleep time in seconds
longTime = 0.5		# Long time for timer events
longTicks = longTime/sleepyTime

eq = EventQueue()
mpdh = MpdHandler(eq)

source = [ Lirc(eq), IrRc(eq), Rotary(eq, sleepyTime), WebSockHandler(eq) ]
handler = [ mpdh, UiHandler(eq, mpdh), SysHandler(eq), NetHandler(eq) ]

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
		Dbg_Print(10, e)
		for h in handler:
			if not handled:
				handled = h.Event(e)
		e = eq.GetEvent()

	#
	count += 1
	if count >= longTicks:
		Dbg_Print(20, "Timer event")
		for s in source:
			s.Timer()
		for h in handler:
			h.Timer()
		count = 0
