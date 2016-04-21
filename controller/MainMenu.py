#!/usr/bin/python
#
# MainMenu.py - the main menu
#
# (c) David Haworth
from Menu import Menu, MenuThing
from Config import Config
import os

class MainMenu(Menu):
	def __init__(self, mh, lcd):
		Menu.__init__(self, mh, lcd)
		cfg = Config()
		self.music_dir = cfg.music_dir
		self.ext_mount = os.path.join(self.music_dir, cfg.music_ext)
		self.things.append(MenuThing('Clear playlist',	self.ClearPlaylist,		''))
		self.things.append(MenuThing('Add to playlist',	self.EnterBrowser,		''))
		self.things.append(MenuThing('Manage playlist',	self.ManagePlaylist,	''))
		self.things.append(MenuThing('Mount external',	self.MountExternal,		''))
		self.things.append(MenuThing('Umount external',	self.UmountExternal,	''))
		self.things.append(MenuThing('MPD options',		self.MpdOptions,		''))
		self.things.append(MenuThing('Test',			self.Test,				''))

	def ClearPlaylist(self, mt, evt):
		if evt == 'ok':
			print "MainMenu.ClearPlaylist()"		# DBG
			self.mh.mpd.mpdc.clear()
			self.Ack()
			return True
		return False

	def EnterBrowser(self, mt, evt):
		if evt == 'ok' or evt == 'right':
			print "MainMenu.EnterBrowser()"
			self.mh.EnterBrowser(self.music_dir)
			return True
		return False

	def ManagePlaylist(self, mt, evt):
		print "MainMenu.ManagePlaylist()"
		return False

	def MountExternal(self, mt, evt):
		if evt == 'ok':
			print "MainMenu.MountExternal()"
			self.mh.EnterMountMenu()
			return True
		return False

	def UmountExternal(self, mt, evt):
		if evt == 'ok':
			print "MainMenu.UMountExternal()"
			if os.path.isfile(os.path.join(self.ext_mount, '___NOT_MOUNTED___')):
				self.Ack()
			else:
				e = os.system('sudo umount ' + self.ext_mount)
				if e == 0:
					self.Ack()
				else:
					print 'Failed to umount ' + self.ext_mount
			return True
		return False

	def MpdOptions(self, mt, evt):
		print "MainMenu.MpdOptions()"
		return False

	def Test(self, mt, evt):
		if evt == 'ok':
			print "MainMenu.Test()"
			self.mh.AskYesNo(['Really?'])
			return True
		if evt == 'ans.yes':
			print "MainMenu.Test() " + evt
			self.Ack()
			return True
		if evt == 'ans.no':
			print "MainMenu.Test() " + evt
			return True
		return False
