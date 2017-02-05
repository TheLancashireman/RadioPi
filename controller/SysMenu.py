#!/usr/bin/python
#
# SysMenu.py - the main menu
#
# (c) David Haworth
from Menu import Menu, MenuThing
from Config import radiopi_cfg
from RadioPiLib import Dbg_Print
import os

class SysMenu(Menu):
	def __init__(self, ui, lcd, eq):
		Menu.__init__(self, ui, lcd, eq)
		self.things.append(MenuThing("Back",			self.Back,				""))
		self.things.append(MenuThing("Restart mpd",  	self.Shutdown,			"m"))
		self.things.append(MenuThing("Exit & restart",	self.Shutdown,			"e"))
		self.things.append(MenuThing("Reboot",			self.Shutdown,			"r"))
		self.things.append(MenuThing("Shut down",		self.Shutdown,			""))
		self.things.append(MenuThing("MPD options",		self.MpdOptions,		""))
		self.things.append(MenuThing("Test",			self.Test,				""))

	def MpdOptions(self, mt, evt):
		Dbg_Print(5, "SysMenu.MpdOptions()")
		return False

	def Test(self, mt, evt):
		if evt == "ok":
			Dbg_Print(5, "SysMenu.Test()")
			self.ui.AskYesNo(["Really?"])
			return True
		if evt == "ans.yes":
			Dbg_Print(5, "SysMenu.Test()", evt)
			self.ui.ShowMessage(["Oh, all right then"], "")
			self.Ack()
			return True
		if evt == "ans.no":
			Dbg_Print(5, "SysMenu.Test()", evt)
			self.ui.ShowMessage(["What do you mean,", "\"No\"?"], "OK")
			return True
		return False

	def Shutdown(self, mt, evt):
		if evt == "ok":
			Dbg_Print(5, "SysMenu.Shutdown()")
			if mt.data == "m":
				self.ui.AskYesNo(["Restart mpd?"])
			elif mt.data == "e":
				self.ui.AskYesNo(["Really exit?"])
			elif mt.data == "r":
				self.ui.AskYesNo(["Really reboot?"])
			else:
				self.ui.AskYesNo(["Really shut down?"])
			return True
		if evt == "ans.yes":
			Dbg_Print(5, "SysMenu.Shutdown() ", evt)
			if mt.data == "m":
				Dbg_Print(1, "Restart mpd")
				self.eq.PutEvent("restartmpd")
			elif mt.data == "e":
				self.ui.ShowMessage(["Restarting RadioPi", "Please wait..."], "")
				Dbg_Print(1, "Restart")
				self.eq.PutEvent("restart")
			elif mt.data == "r":
				self.ui.ShowMessage(["Rebooting", "Please wait..."], "")
				Dbg_Print(1, "Reboot")
				self.eq.PutEvent("reboot")
			else:
				self.ui.ShowMessage(["Shutting down", "Bye..."], "")
				Dbg_Print(1, "Shutdown")
				self.eq.PutEvent("shutdown")
			return True
		if evt == "ans.no":
			Dbg_Print(5, "SysMenu.Shutdown()", evt)
			return True
		return False
