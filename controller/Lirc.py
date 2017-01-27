#!/usr/bin/python
#
# Lirc I/R Remote Control input
#
# (c) David Haworth

import lirc

class Lirc:
	def __init__(self, eq):
		self.eq = eq
		self.sockid = lirc.init("RadioPi", "/home/pi/RadioPi/lirc/lircrc-piremote", blocking=False)

	def Timer(self):					# Called infrequently to update status.
		return False

	def Poll(self):						# Called frequently to read keys from remote control.
		while True:
			klist = lirc.nextcode()
			if len(klist) == 0:
				return False
			for k in klist:
				if k != "":
					self.eq.PutEvent(k)
		return False
