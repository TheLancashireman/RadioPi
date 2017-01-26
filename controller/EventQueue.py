#!/usr/bin/python
#
# Event queue management
#
# (c) David Haworth

class EventQueue:
	def __init__(self):
		self.events = []

	def GetEvent(self):
		e = ""
		if len(self.events) > 0:
			e = self.events[0]
			self.events = self.events[1:len(self.events)]
		return e

	def PutEvent(self, e):
		self.events.append(e)
