#!/usr/bin/python
#
# MainMenu.py - the main menu
#
# (c) David Haworth
from Menu import Menu, MenuThing

class MainMenu(Menu):
	def __init__(self, mh, lcd):
		Menu.__init__(self, mh, lcd)
		self.things.append(MenuThing('Clear playlist',	self.ClearPlaylist,		''))
		self.things.append(MenuThing('Add to playlist',	self.EnterBrowser,		''))
		self.things.append(MenuThing('Manage playlist',	self.ManagePlaylist,	''))
		self.things.append(MenuThing('Mount external',	self.MountExternal,		''))
		self.things.append(MenuThing('Umount external',	self.UmountExternal,	''))
		self.things.append(MenuThing('MPD options',		self.MpdOptions,		''))

	def ClearPlaylist(self, mt, evt):
		if evt == 'ok':
			print "MainMenu.ClearPlaylist()"
			self.mh.mpd.mpdc.clear()
			return True
		return False

	def EnterBrowser(self, mt, evt):
		if evt == 'ok' or evt == 'right':
			print "MainMenu.EnterBrowser()"
			self.mh.EnterBrowser('/home/pi/Music')
			return True
		return False

	def ManagePlaylist(self, mt, evt):
		print "MainMenu.ManagePlaylist()"
		return False

	def MountExternal(self, mt, evt):
		print "MainMenu.MountExternal()"
		return False

	def UmountExternal(self, mt, evt):
		print "MainMenu.UMountExternal()"
		return False

	def MpdOptions(self, mt, evt):
		print "MainMenu.MpdOptions()"
		return False
