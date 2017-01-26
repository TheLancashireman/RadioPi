#!/usr/bin/python
#
# SysHandler.py - event handler for system commands
#
# (c) David Haworth

import os
from Config import radiopi_cfg

class SysHandler:
	def __init__(self, eq):
		self.eq = eq
		return

	# Event handler
	def Event(self, evt):
		if evt == 'shutdown':
			os.system("sudo shutdown -h now")
			return True

		if evt == 'reboot':
			os.system("sudo shutdown -r now")
			return True

		if evt == 'restart':
			exit(0)
			return True

		if evt[0:6] == "mount ":
			print "SysHandler:", evt
			dev = evt[6:len(evt)]
			mountpoint = os.path.join(radiopi_cfg.music_dir, radiopi_cfg.music_ext)
			if os.path.isfile(os.path.join(mountpoint, '___NOT_MOUNTED___')):
				os.system("sudo mount -o ro " + dev + " " + mountpoint)
			return True

		if evt == "umount":
			mountpoint = os.path.join(radiopi_cfg.music_dir, radiopi_cfg.music_ext)
			if not os.path.isfile(os.path.join(mountpoint, '___NOT_MOUNTED___')):
				os.system("sudo umount " + mountpoint)
			return True

		return False

	# Timer handler - nothing to do
	def Timer(self):
		return False
