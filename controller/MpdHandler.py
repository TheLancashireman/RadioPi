#!/usr/bin/python
#
# MpdHandler.py - event handler for MPD
#
# (c) David Haworth

import os
import mpd
from mpd import MPDClient
from RadioPiLib import Dbg_Print

class MpdHandler:
	def __init__(self, eq):
		self.eq = eq
		Dbg_Print(5, "self.mpdc = MPDClient()")
		self.mpdc = MPDClient()
		self.mpdConnected = False
		self.eventmap = {
			"vol+"	: self.VolumeUp,
			"vol-"	: self.VolumeDown,
			">/||"	: self.TogglePlayPause,
			"stop"	: self.Stop,
			"|<"	: self.SkipBack,
			">|"	: self.SkipForward,
			"<<"	: self.SeekBack,
			">>"	: self.SeekForward,
			"clear"	: self.ClearPlaylist	}

		self.MpdConnect()

	def MpdConnect(self):
		try:						# Try to connect
			self.mpdc.timeout = 100
			self.mpdc.idletimeout = None
			Dbg_Print(5, "self.mpdc.connect(\"/run/mpd/socket\", 6600)")
			self.mpdc.connect("/run/mpd/socket", 6600)
			self.mpdConnected = True
		except mpd.ConnectionError:
			self.mpdConnected = False

	def VolumeUp(self):
		Dbg_Print(5, "self.mpdc.status()")
		s = self.mpdc.status()
		v = int(s["volume"])
		if v < 100:					# Increase volume if < 100.
			Dbg_Print(5, "self.mpdc.setvol(v+1)")
			self.mpdc.setvol(v+1)

	def VolumeDown(self):
		Dbg_Print(5, "self.mpdc.status()")
		s = self.mpdc.status()
		v = int(s["volume"])
		if v > 0:					# Reduce volume if > 0.
			Dbg_Print(5, "self.mpdc.setvol(v-1)")
			self.mpdc.setvol(v-1)

	def TogglePlayPause(self):
		Dbg_Print(5, "self.mpdc.status()")
		s = self.mpdc.status()
		if s["state"] == "stop":	# Play if stopped.
			Dbg_Print(5, "self.mpdc.play()")
			self.mpdc.play()
		else:						# Toggle play/pause if playing or paused.
			Dbg_Print(5, "self.mpdc.pause()")
			self.mpdc.pause()

	def Stop(self):
		Dbg_Print(5, "self.mpdc.stop()")
		self.mpdc.stop()

	def SkipBack(self):
		Dbg_Print(5, "self.mpdc.status()")
		s = self.mpdc.status()
		if s["state"] == "stop":
			Dbg_Print(5, "self.mpdc.previous()")
			self.mpdc.previous()
		else:
			t = int(float(s["elapsed"]))
			if t < 5:					# Go to previous track if near start of track.
				Dbg_Print(5, "self.mpdc.previous()")
				self.mpdc.previous()	# Restarts track if first in list.
			else:						# Go to start of track if not near beginning.
				Dbg_Print(5, "self.mpdc.seekcur(0)")
				self.mpdc.seekcur(0)

	def SkipForward(self):
		Dbg_Print(5, "self.mpdc.next()")
		self.mpdc.next()

	def SeekBack(self):
		Dbg_Print(5, "self.mpdc.status()")
		s = self.mpdc.status()
		if s["state"] != "stop":
			Dbg_Print(5, "self.mpdc.seekcur(\"-10\")")
			self.mpdc.seekcur("-10")

	def SeekForward(self):
		Dbg_Print(5, "self.mpdc.status()")
		s = self.mpdc.status()
		if s["state"] != "stop":
			Dbg_Print(5, "self.mpdc.seekcur(\"+10\")")
			self.mpdc.seekcur("+10")

	def ClearPlaylist(self):
		Dbg_Print(5, "self.mpdc.clear()")
		self.mpdc.clear()

	def Add(self, ff):
		if os.path.isfile(ff):
			Dbg_Print(5, "add file", ff)
			Dbg_Print(5, "self.mpdc.add(\"file://\"+ff)")
			self.mpdc.add("file://"+ff)
		elif os.path.isdir(ff):
			Dbg_Print(5, "add album", ff)
			files = os.listdir(ff)
			files.sort()
			for f in files:
				fff = os.path.join(ff, f)
				Dbg_Print(5, "add file", fff)
				Dbg_Print(5, "self.mpdc.add(\"file://\"+fff)")
				self.mpdc.add("file://"+fff)

	def PlayUrl(self, url):
		Dbg_Print(5, "Radio station ", url)
		self.Stop()
		self.ClearPlaylist()
		Dbg_Print(5, "self.mpdc.add(url)")
		self.mpdc.add(url)
		Dbg_Print(5, "self.mpdc.play()")
		self.mpdc.play()

	# Event handler
	def Event(self, evt):
		if evt == "restartmpd":
			Dbg_Print(1, "Restart mpd")
			os.system("sudo /etc/init.d/mpd restart")
			self.mpdConnected = False
			return True

		if not self.mpdConnected:
			self.MpdConnect()
		if self.mpdConnected:
			if evt in self.eventmap.keys():
				try:
					self.eventmap[evt]()
				except mpd.ConnectionError:
					self.mpdConnected = False
				return True
			elif evt[0:4] == "add ":
				self.Add(evt[4:len(evt)])
				return True
			elif evt[0:8] == "station ":
				self.PlayUrl(evt[8:len(evt)])
				return True
		return False

	# Timer handler - nothing to do
	def Timer(self):
		return False

	def Status(self):
		s = {}
		if not self.mpdConnected:
			self.MpdConnect()
		if self.mpdConnected:
			try:
				Dbg_Print(5, "self.mpdc.status()")
				s = self.mpdc.status()
			except:
				pass
		return s

	def CurrentSong(self):
		s = {}
		if not self.mpdConnected:
			self.MpdConnect()
		if self.mpdConnected:
			try:
				Dbg_Print(5, "self.mpdc.currentsong()")
				s = self.mpdc.currentsong()
			except:
				pass
		return s
