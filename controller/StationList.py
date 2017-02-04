#!/usr/bin/python
#
# StationList.py - menu containing list of favourite internet radio stations from file
#
# (c) David Haworth

from Menu import Menu, MenuThing
from Config import radiopi_cfg
from RadioPiLib import Dbg_Print
import string


class StationList(Menu):
	def __init__(self, ui, lcd, eq):
		Menu.__init__(self, ui, lcd, eq)
		self.things.append(MenuThing('Back',	self.Back,		''))

		sl = open(radiopi_cfg.stationlist, "r")
		for line in sl:
			if line[0] != "#":
				line = string.rstrip(string.lstrip(line))	# Remove leading and trailing whitespace (incl. newline)
				if string.find(line, "|") > 0:
					name,url = string.split(line, "|")
					self.things.append((MenuThing(name, self.SelectStation, url)))
		sl.close()

	def SelectStation(self, mt, evt):
		if evt == 'ok':
			Dbg_Print(2, "StationList", mt.data)
			self.eq.PutEvent("station " + mt.data)
			self.Ack()
			return True
		return False
