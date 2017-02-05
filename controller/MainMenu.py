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
		self.things.append(MenuThing("Network menu",	self.EnterNetMenu,		""))
		self.things.append(MenuThing("System menu",		self.EnterSysMenu,		""))
		self.things.append(MenuThing("Manage playlist",	self.ManagePlaylist,	""))

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

	def EnterNetMenu(self, mt, evt):
		if evt == "ok" or evt == "right":
			Dbg_Print(5, "MainMenu.EnterNetMenu()")
			self.ui.EnterNetMenu()
			return True
		return False

	def EnterSysMenu(self, mt, evt):
		if evt == "ok" or evt == "right":
			Dbg_Print(5, "MainMenu.EnterSysMenu()")
			self.ui.EnterSysMenu()
			return True
		return False
