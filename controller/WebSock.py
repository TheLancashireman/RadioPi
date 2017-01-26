#!/usr/bin/python
#
# Web socket input
#
# (c) David Haworth

import os
from SimpleWebSocketServer_dh import SimpleWebSocketServer, WebSocket
from Config import radiopi_cfg
from RadioPiLib import MountableDevs

port_no = 6502
evtq = 0

valid_cmd = ['vol+', 'vol-', '>/||', 'stop', '|<', '>|', '<<', '>>', 'clear', 'shutdown', 'reboot', 'restart', 'restartmpd', 'umount']


class WebSockHandler(WebSocket):
	def __init__(self, eq):
		global evtq
		evtq = eq
		print "Starting websocket server on localhost:%d" % port_no
		self.server = SimpleWebSocketServer("", port_no, WebSock)
		self.server.selectInterval = 0.0

	def Timer(self):				# Called infrequently to update status.
		return False

	def Poll(self):					# Called frequently to read commands from browser(s)
		self.server.serveonce()		# Poll for commands via socket.
		return False

class WebSock(WebSocket):
	def handleMessage(self):
		msg = self.data
		print "WebSock command:", msg
		if msg in valid_cmd:
			evtq.PutEvent(msg)
		elif msg[0:4] == "add ":
			npath = os.path.normpath(os.path.join(radiopi_cfg.music_dir, msg[4:len(msg)]))
			if npath[0:len(radiopi_cfg.music_dir)] == radiopi_cfg.music_dir:
				if os.path.isfile(npath) or os.path.isdir(npath):
					evtq.PutEvent("add " + npath)
				else:
					print "Websock invalid path:", msg
			else:
				"Websock attempt to break out of jail:", msg
		elif msg[0:6] == "mount ":
			d = msg[6:len(msg)]
			devs = MountableDevs("/dev")
			if d in devs:
				evtq.PutEvent("mount " + os.path.join("/dev", d))
			else:
				print "Websock invalid device:", msg
		else:
			print "WebSock invalid command:", msg

	def handleConnected(self):
		print "WebSock", self.address, "connected"

	def handleClose(self):
		print "WebSock", self.address, "closed"
