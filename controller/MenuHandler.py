#!/usr/bin/python
#
# MenuHandler.py - handler for the display
#
# (c) David Haworth

from MainMenu import MainMenu

class MenuHandler:
	def __init__(self, mpd, lcd):
		self.mpd = mpd				# MPD handler
		self.lcd = lcd				# Display handler
		self.menu = MainMenu(self)	#
		self.ptrpos = 0				# Item where the pointer is.
		self.top = 0				# Item at top of screen.

	def Enter(self):
		self.menu = MainMenu(self)
		self.ptrpos = 0
		self.top = 0
		self.Show()

	def Event(self, evt):
		return False

	def Show(self):
		nrows = self.lcd.GetNRows()
		mnu = self.menu
		j = self.top
		for i in range(nrows):
			if i == 0:
				self.lcd.HomeAndClear()
			else:
				self.lcd.NewLine()
			self.lcd.Write(' ' + mnu.Item(j))
			j += 1
		if self.ptrpos >= self.top and self.ptrpos < (self.top + nrows):
			line = self.ptrpos - self.top + 1
			self.lcd.Write(self.lcd.GoStr(line,1)+'\x7e\r')

	def ClearPlaylist(self):
		print 'MenuHandler.ClearPlaylist'
		mpd.Clear()

	def AddTracks(self):
		print 'MenuHandler.AddTracks'
		return 0

	def ManagePlaylist(self):
		print 'MenuHandler.ManagePlaylist'
		return 0

	def MountExternal(self):
		print 'MenuHandler.MountExternal'
		return 0

	def UmountExternal(self):
		print 'MenuHandler.UmountExternal'
		return 0

	def MpdOptions(self):
		print 'MenuHandler.MpdOptions'
		return 0

	def Foo(self):
		print 'MenuHandler.Foo'
		return 0
