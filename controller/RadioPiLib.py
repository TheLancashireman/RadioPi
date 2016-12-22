#!/usr/bin/python
#
# RadioPiLib.py - assorted library functions
#
# (c) David Haworth

import os
import stat
from Config import radiopi_cfg

# Print message if debug level exceeds threshold.
def Dbg_Print(l,x):
	if l <= radiopi_cfg.dbg_level:
		print "RadioPi Dbg:", x

# Return a list of mountable block devices in given directory
def MountableDevs(d):
	lastdev = "/"
	devs = []
	dlist = os.listdir(d)
	dlist.sort()
	for f in dlist:
		df = os.path.join(d, f)
		if not ( f.startswith('ram') or f.startswith('loop') or f.startswith('mmcblk0') ):
			if stat.S_ISBLK(os.stat(df).st_mode):
				if not f.startswith(lastdev):
					if lastdev != "/":
						devs.append(lastdev)
				lastdev = f
	if lastdev != "/":
		devs.append(lastdev)
	return devs
