#!/usr/bin/python
#
# MainMenu.py - the main menu
#
# (c) David Haworth
from Menu import Menu, MenuThing
from Config import radiopi_cfg
from RadioPiLib import Dbg_Print
import os

class MainMenu(Menu):
	def __init__(self, ui, lcd, eq):
		Menu.__init__(self, ui, lcd, eq)
		self.things.append(MenuThing("Back",			self.Back,				""))
		self.things.append(MenuThing("Clear playlist",	self.ClearPlaylist,		""))
		self.things.append(MenuThing("Add to playlist",	self.EnterBrowser,		""))
		self.things.append(MenuThing("Internet radio",	self.SelectStation,		""))
		self.things.append(MenuThing("Mount external",	self.MountExternal,		""))
		self.things.append(MenuThing("Umount external",	self.UmountExternal,	""))
		self.things.append(MenuThing("Exit & restart",	self.Shutdown,			"e"))
		self.things.append(MenuThing("Reboot",			self.Shutdown,			"r"))
		self.things.append(MenuThing("Shut down",		self.Shutdown,			""))
		self.things.append(MenuThing("MPD options",		self.MpdOptions,		""))
		self.things.append(MenuThing("Manage playlist",	self.ManagePlaylist,	""))
		self.things.append(MenuThing("Test",			self.Test,				""))

	def ClearPlaylist(self, mt, evt):
		if evt == "ok":
			Dbg_Print(5, "MainMenu.ClearPlaylist()")
			self.eq.PutEvent("clear")
			self.Ack()
			return True
		return False

	def EnterBrowser(self, mt, evt):
		if evt == "ok" or evt == "right":
			Dbg_Print(5, "MainMenu.EnterBrowser()")
			self.ui.EnterBrowser(radiopi_cfg.music_dir)
			return True
		return False

	def SelectStation(self, mt, evt):
		if evt == "ok" or evt == "right":
			Dbg_Print(5, "MainMenu.SelectStation()")
			self.ui.EnterStationList()
			return True
		return False

	def ManagePlaylist(self, mt, evt):
		Dbg_Print(5, "MainMenu.ManagePlaylist()")
		return False

	def MountExternal(self, mt, evt):
		if evt == "ok":
			Dbg_Print(5, "MainMenu.MountExternal()")
			self.ui.EnterMountMenu()
			return True
		return False

	def UmountExternal(self, mt, evt):
		if evt == "ok":
			Dbg_Print(5, "MainMenu.UMountExternal()")
			self.eq.PutEvent("umount")
			self.Ack()
			return True
		return False

	def MpdOptions(self, mt, evt):
		Dbg_Print(5, "MainMenu.MpdOptions()")
		return False

	def Test(self, mt, evt):
		if evt == "ok":
			Dbg_Print(5, "MainMenu.Test()")
			self.ui.AskYesNo(["Really?"])
			return True
		if evt == "ans.yes":
			Dbg_Print(5, "MainMenu.Test()", evt)
			self.ui.ShowMessage(["Oh, all right then"], "")
			self.Ack()
			return True
		if evt == "ans.no":
			Dbg_Print(5, "MainMenu.Test()", evt)
			self.ui.ShowMessage(["What do you mean,", "\"No\"?"], "OK")
			return True
		return False

	def Shutdown(self, mt, evt):
		if evt == "ok":
			Dbg_Print(5, "MainMenu.Shutdown()")
			if mt.data == "e":
				self.ui.AskYesNo(["Really exit?"])
			elif mt.data == "r":
				self.ui.AskYesNo(["Really reboot?"])
			else:
				self.ui.AskYesNo(["Really shut down?"])
			return True
		if evt == "ans.yes":
			Dbg_Print(5, "MainMenu.Shutdown() ", evt)
			if mt.data == "e":
				self.ui.ShowMessage(["Restarting RadioPi", "Please wait..."], "")
				Dbg_Print(1, "Restart")
				exit(0)
			elif mt.data == "r":
				self.ui.ShowMessage(["Rebooting", "Please wait..."], "")
				Dbg_Print(1, "Reboot")
				os.system("sudo reboot")
			else:
				self.ui.ShowMessage(["Shutting down", "Bye..."], "")
				Dbg_Print(1, "Shutdown")
				os.system("sudo shutdown -h now")
			return True
		if evt == "ans.no":
			Dbg_Print(5, "MainMenu.Shutdown()", evt)
			return True
		return False
