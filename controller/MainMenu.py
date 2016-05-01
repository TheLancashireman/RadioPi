#!/usr/bin/python
#
# MainMenu.py - the main menu
#
# (c) David Haworth
from Menu import Menu, MenuThing
from Config import Config
import os

class MainMenu(Menu):
	def __init__(self, ui, lcd):
		Menu.__init__(self, ui, lcd)
		cfg = Config()
		self.music_dir = cfg.music_dir
		self.ext_mount = os.path.join(self.music_dir, cfg.music_ext)
		self.things.append(MenuThing('Clear playlist',	self.ClearPlaylist,		''))
		self.things.append(MenuThing('Add to playlist',	self.EnterBrowser,		''))
		self.things.append(MenuThing('Mount external',	self.MountExternal,		''))
		self.things.append(MenuThing('Umount external',	self.UmountExternal,	''))
		self.things.append(MenuThing('Exit & restart',	self.Shutdown,			'e'))
		self.things.append(MenuThing('Reboot',			self.Shutdown,			'r'))
		self.things.append(MenuThing('Shut down',		self.Shutdown,			''))
		self.things.append(MenuThing('MPD options',		self.MpdOptions,		''))
		self.things.append(MenuThing('Manage playlist',	self.ManagePlaylist,	''))
		self.things.append(MenuThing('Test',			self.Test,				''))

	def ClearPlaylist(self, mt, evt):
		if evt == 'ok':
			print "MainMenu.ClearPlaylist()"		# DBG
			self.ui.mpd.mpdc.clear()
			self.Ack()
			return True
		return False

	def EnterBrowser(self, mt, evt):
		if evt == 'ok' or evt == 'right':
			print "MainMenu.EnterBrowser()"
			self.ui.EnterBrowser(self.music_dir)
			return True
		return False

	def ManagePlaylist(self, mt, evt):
		print "MainMenu.ManagePlaylist()"
		return False

	def MountExternal(self, mt, evt):
		if evt == 'ok':
			print "MainMenu.MountExternal()"
			self.ui.EnterMountMenu()
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
			self.ui.AskYesNo(['Really?'])
			return True
		if evt == 'ans.yes':
			print "MainMenu.Test() " + evt
			self.ui.ShowMessage(['Oh, all right then'], '')
			self.Ack()
			return True
		if evt == 'ans.no':
			print "MainMenu.Test() " + evt
			self.ui.ShowMessage(['What do you mean,', '"No"?'], 'OK')
			return True
		return False

	def Shutdown(self, mt, evt):
		if evt == 'ok':
			print "MainMenu.Shutdown()"
			if mt.data == 'e':
				self.ui.AskYesNo(['Really exit?'])
			elif mt.data == 'r':
				self.ui.AskYesNo(['Really reboot?'])
			else:
				self.ui.AskYesNo(['Really shut down?'])
			return True
		if evt == 'ans.yes':
			print "MainMenu.Shutdown() " + evt
			if mt.data == 'e':
				self.ui.ShowMessage(['Restarting RadioPi', 'Please wait...'], '')
				exit(0)
			elif mt.data == 'r':
				self.ui.ShowMessage(['Rebooting', 'Please wait...'], '')
				os.system('sudo reboot')
			else:
				self.ui.ShowMessage(['Shutting down', 'Bye...'], '')
				os.system('sudo shutdown -h now')
			return True
		if evt == 'ans.no':
			print "MainMenu.Shutdown() " + evt
			return True
		return False
