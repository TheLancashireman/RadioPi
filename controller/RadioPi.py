#!/usr/bin/python
#
# RadioPi.py - RadioPi main control program
#
# (c) David Haworth

from MpdHandler import MpdHandler
from UiHandler import UiHandler
from IrRc import IrRc
from WebSock import WebSockHandler
import time

handler = [ MpdHandler() ]
handler.append(UiHandler(handler[0]))

source = [ IrRc(), WebSockHandler() ]

count = 0

while True:
#	time.sleep(0.05)
	for s in source:
		e = s.GetEvent()
		handled = False
		if e != '':
			print e		# Debug
			for h in handler:
				if not handled:
					handled = h.Event(e)
	count += 1
	if count >= 20:
		#print 'Timer event'
		for s in source:
			s.Timer()
		for h in handler:
			h.Timer()
		count = 0
