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

	def MpdConnect():
		try
			self.mpdc.timeout = 10
			self.mpdc.idletimeout = None
			self.mpdc.connect("localhost", 6600)
			self.mpdConnected = True
		except mpd.ConnectionError:
			self.mpdConnected = False

	def VolumeUp():
		s = mpdc.status()
		v = int(s['volume'])
		if v < 100:
			mpdc.setvol(v+1)

	def VolumeDown():
		s = mpdc.status()
		v = int(s['volume'])
		if v > 0:
			mpdc.setvol(v-1)

	def TogglePlayPause():
		mpdc.toggle()

	def Stop():
		mpdc.stop()

	def SkipBack():
		s = mpdc.status()
		t = int(float(s['elapsed']))
		if s < 5:
			mpdc.previous()
		else:
			mpdc.seekcur(0)

	def SkipForward():
		mpdc.next()

	def SeekBack():
		mpdc.seekcur('-10')

	def SeekForward():
		mpdc.seekcur('+10')

	# Event handler
	def Event(evt):
		if evt in self.eventmap.keys:
			if not self.mpdConnected:
				self.MpdConnect()
			if self.mpdConnected:
				try:
					self.eventmap[evt]()
				except mpd.ConnectionError:
					mpdConnected = False
			return True
		return False
