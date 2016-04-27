#!/usr/bin/python
#
# MountMenu.py - browser menu for block devices to mount
#
# (c) David Haworth

from Menu import Menu, MenuThing
from Config import Config
import os
import stat

class MountMenu(Menu):
	def __init__(self, ui, lcd):
		Menu.__init__(self, ui, lcd)
		self.things.append(MenuThing('Back',	self.Back,		''))
		devdir = '/dev'

		devs = os.listdir(devdir)
		devs.sort()

		for f in devs:
			ff = os.path.join(devdir, f)
			if stat.S_ISBLK(os.stat(ff).st_mode):
				if not ( f.startswith('ram') or f.startswith('loop') or f.startswith('mmcblk0') ):
					self.things.append(MenuThing(f,	self.MountDev, ff))

	def Back(self, mt, evt):
		if evt == 'ok':
			self.ui.Back()
			return True
		return False

	def MountDev(self, mt, evt):
		if evt == 'ok':
			cfg = Config()
			mountpoint = os.path.join(cfg.music_dir, cfg.music_ext)
			if not os.path.isfile(os.path.join(mountpoint, '___NOT_MOUNTED___')):
				e = os.system('sudo umount ' + mountpoint)
				if e != 0:
					print 'Failed to umount ' + mountpoint
			e = os.system('sudo mount -o ro ' + mt.data + ' ' + mountpoint)
			if e == 0:
				self.Ack()
			else:
				print 'Failed to mount ' + mt.data + ' on ' + mountpoint
			return True
		return False
