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
		self.mpdc = MPDClient()
		self.mpdConnected = False
		self.eventmap = {
			'vol+'	: self.VolumeUp,
			'vol-'	: self.VolumeDown,
			'>/||'	: self.TogglePlayPause,
			'stop'	: self.Stop,
			'|<'	: self.SkipBack,
			'>|'	: self.SkipForward,
			'<<'	: self.SeekBack,
			'>>'	: self.SeekForward,
			'clear'	: self.ClearPlaylist	}

		self.MpdConnect()

	def MpdConnect(self):
		try:						# Try to connect
			self.mpdc.timeout = 100
			self.mpdc.idletimeout = None
			self.mpdc.connect('/run/mpd/socket', 6600)
			self.mpdConnected = True
		except mpd.ConnectionError:
			self.mpdConnected = False

	def VolumeUp(self):
		s = self.mpdc.status()
		v = int(s['volume'])
		if v < 100:					# Increase volume if < 100.
			self.mpdc.setvol(v+1)

	def VolumeDown(self):
		s = self.mpdc.status()
		v = int(s['volume'])
		if v > 0:					# Reduce volume if > 0.
			self.mpdc.setvol(v-1)

	def TogglePlayPause(self):
		s = self.mpdc.status()
		if s['state'] == 'stop':	# Play if stopped.
			self.mpdc.play()
		else:						# Toggle play/pause if playing or paused.
			self.mpdc.pause()

	def Stop(self):
		self.mpdc.stop()

	def SkipBack(self):
		s = self.mpdc.status()
		if s['state'] == 'stop':
			self.mpdc.previous()
		else:
			t = int(float(s['elapsed']))
			if t < 5:					# Go to previous track if near start of track.
				self.mpdc.previous()	# Restarts track if first in list.
			else:						# Go to start of track if not near beginning.
				self.mpdc.seekcur(0)

	def SkipForward(self):
		self.mpdc.next()

	def SeekBack(self):
		s = self.mpdc.status()
		if s['state'] != 'stop':
			self.mpdc.seekcur('-10')

	def SeekForward(self):
		s = self.mpdc.status()
		if s['state'] != 'stop':
			self.mpdc.seekcur('+10')

	def ClearPlaylist(self):
		self.mpdc.clear()

	def Add(self, ff):
		if os.path.isfile(ff):
			Dbg_Print(5, "add file", ff)
			self.mpdc.add("file://"+ff)
		elif os.path.isdir(ff):
			Dbg_Print(5, "add album", ff)
			files = os.listdir(ff)
			files.sort()
			for f in files:
				fff = os.path.join(ff, f)
				self.mpdc.add('file://'+fff)

	# Event handler
	def Event(self, evt):
		if evt == 'restartmpd':
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
				s = self.mpdc.currentsong()
			except:
				pass
		return s
