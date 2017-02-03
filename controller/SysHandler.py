#!/usr/bin/python
#
# SysHandler.py - event handler for system commands
#
# (c) David Haworth

import os
from Config import radiopi_cfg
from RadioPiLib import Dbg_Print

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
			Dbg_Print(5, "SysHandler:", evt)
			dev = evt[6:len(evt)]
			mountpoint = os.path.join(radiopi_cfg.music_dir, radiopi_cfg.music_ext)
			if not os.path.isfile(os.path.join(mountpoint, '___NOT_MOUNTED___')):
				e = os.system("sudo umount " + mountpoint)
				if e == 0:
					Dbg_Print(1, "Umounted", mountpoint)
				else:
					Dbg_Print(0, "Failed to umount", mountpoint)

			e = os.system("sudo mount -o ro " + dev + " " + mountpoint)
			if e == 0:
				Dbg_Print(1, "Mounted", dev, "on", mountpoint)
			else:
				Dbg_Print(0, "Failed to mount", dev, "on", mountpoint)

			return True

		if evt == "umount":
			mountpoint = os.path.join(radiopi_cfg.music_dir, radiopi_cfg.music_ext)
			if os.path.isfile(os.path.join(mountpoint, '___NOT_MOUNTED___')):
				Dbg_Print(0, mountpoint, "not mounted")
			else:
				os.system("sudo umount " + mountpoint)
				Dbg_Print(1, "Umounted", mountpoint)
			return True

		return False

	# Timer handler - nothing to do
	def Timer(self):
		return False
