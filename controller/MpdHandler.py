#!/usr/bin/python
#
# MpdHandler.py - event handler for MPD
#
# (c) David Haworth
import mpd
from mpd import MPDClient

class MpdHandler:
	def __init__(self):
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
			'>>'	: self.SeekForward	}

		self.MpdConnect()

	def MpdConnect(self):
		try:						# Try to connect
			self.mpdc.timeout = 10
			self.mpdc.idletimeout = None
			self.mpdc.connect("localhost", 6600)
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

	# Event handler
	def Event(self, evt):
		if evt in self.eventmap.keys():
			if not self.mpdConnected:
				self.MpdConnect()
			if self.mpdConnected:
				try:
					self.eventmap[evt]()
				except mpd.ConnectionError:
					self.mpdConnected = False
			return True
		return False
