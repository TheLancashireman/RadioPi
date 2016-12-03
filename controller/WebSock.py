#!/usr/bin/python
#
# Web socket input
#
# (c) David Haworth

from SimpleWebSocketServer_dh import SimpleWebSocketServer, WebSocket

port_no = 6502

events = []

class WebSockHandler(WebSocket):
	def __init__(self):
		print "Starting websocket server on localhost:%d" % port_no
		self.server = SimpleWebSocketServer("", port_no, WebSock)

	def Timer(self):					# Called infrequently to update status.
		return False

	def GetEvent(self):					# Called frequently to read commands from browser(s)
		global events

		self.server.serveonce()

		if len(events) > 0:
			e = events[0]
			events = events[1:-1]
		else:
			e = ""

		return e

class WebSock(WebSocket):
	def handleMessage(self):
		msg = self.data
		print "WebSock command:", msg

	def handleConnected(self):
		print "WebSock", self.address, "connected"

	def handleClose(self):
		print "WebSock", self.address, "closed"
