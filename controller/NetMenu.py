#!/usr/bin/python
#
# NetMenu.py - the main menu
#
# (c) David Haworth

from Menu import Menu, MenuThing
from Config import radiopi_cfg
from RadioPiLib import Dbg_Print
import os

class NetMenu(Menu):
	def __init__(self, ui, lcd, eq):
		Menu.__init__(self, ui, lcd, eq)
		self.things.append(MenuThing("Back",			self.Back,				""))
		self.things.append(MenuThing("Ethernet",	  	self.Ethernet,			""))

		s = "wpa_supplicant-"
		e = ".conf"
		files = os.listdir("/etc/wpa_supplicant")
		files.sort()
		for f in files:
			if f[0:len(s)] == s and f[-len(e):len(f)] == e:
				self.things.append(MenuThing(f[len(s):-len(e)], self.WiFi, f))

	def Ethernet(self, mt, evt):
		if evt == "ok":
			Dbg_Print(1, "NetMenu.Ethernet()")
			self.eq.PutEvent("ethernet")
			self.Ack()
			return True
		return False

	def WiFi(self, mt, evt):
		if evt == "ok":
			Dbg_Print(1, "NetMenu.WiFi()", mt.data)
			self.eq.PutEvent("wifi " + mt.data)
			self.Ack()
			return True
		return False
