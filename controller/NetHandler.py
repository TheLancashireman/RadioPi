#!/usr/bin/python
#
# NetHandler.py - event handler for network control
#
# (c) David Haworth

import os
from Config import radiopi_cfg
from RadioPiLib import Dbg_Print

class NetHandler:
	def __init__(self, eq):
		self.eq = eq
		return

	# Event handler
	def Event(self, evt):
		if evt == 'ethernet':
			cmd = "sudo " + radiopi_cfg.script_dir + "/ether-up.sh"
			Dbg_Print(1, "NetHandler:", cmd)
			os.system(cmd)
			return True

		if evt[0:5] == "wifi ":
			wpa = evt[5:len(evt)]
			cmd = "sudo " + radiopi_cfg.script_dir + "/wifi-up.sh " + wpa
			Dbg_Print(1, "NetHandler:", cmd)
			os.system(cmd)
			return True

		return False

	# Timer handler - nothing to do
	def Timer(self):
		return False
