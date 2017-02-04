#!/usr/bin/python
#
# MountMenu.py - browser menu for block devices to mount
#
# (c) David Haworth

from Menu import Menu, MenuThing
from Config import radiopi_cfg
from RadioPiLib import MountableDevs, Dbg_Print
import os
import stat

class MountMenu(Menu):
	def __init__(self, ui, lcd, eq):
		Menu.__init__(self, ui, lcd, eq)
		self.things.append(MenuThing("Back",	self.Back,		""))
		devdir = "/dev"

		devs = MountableDevs(devdir)

		for f in devs:
			ff = os.path.join(devdir, f)
			self.things.append(MenuThing(f,	self.MountDev, ff))

	def MountDev(self, mt, evt):
		if evt == "ok":
			self.eq.PutEvent("mount " + mt.data)
			self.Ack()
			return True
		return False
