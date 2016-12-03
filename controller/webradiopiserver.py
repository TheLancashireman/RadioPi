#!/usr/bin/python
#
# webradiopiserver.py - server for webradiopi
#

from SimpleWebSocketServer_dh import SimpleWebSocketServer, WebSocket

port_no = 6502

class WebRadioPiServer(WebSocket):

    def handleMessage(self):
        msg = self.data		# 10 billion sounds should be enough for everyone
        print "command:", msg

    def handleConnected(self):
        print "WebRadioPiServer", self.address, "connected"

    def handleClose(self):
        print "WebRadioPiServer", self.address, "closed"

print "Starting server on localhost:%d" % port_no
server = SimpleWebSocketServer("", port_no, WebRadioPiServer)
server.serveforever()
