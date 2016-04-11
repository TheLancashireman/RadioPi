#!/usr/bin/python
#
# MenuHandler.py - handler for the display
#
# (c) David Haworth

class MenuHandler:
	def __init__(self, lcd, mpd):
		self.lcd = lcd				# Display handler
		self.mpd = mpd				# MPD handler
		self.menu = MainMenu		# Current menu
		self.item = 0				# Item where the pointer is.
		self.top = 0				# Item at top of screen.

	def Enter(self, mode):
		self.menu = MainMenu
		self.item = 0
		self.top = 0
		return mode

	def Event(self, mode, evt):
		return mode

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

class MainMenu:
	def __init__(self, mh):
		self.items = [
			'Clear playlist',
			'Add tracks',
			'Manage playlist',
			'Mount external',
			'Umount external',
			'MPD options',
			'Foo'
		]
		self.actions = [
			mh.ClearPlaylist,
			mh.AddTracks,
			mh.ManagePlaylist,
			mh.MountExternal,
			mh.UmountExternal,
			mh.MpdOptions,
			mh.Foo
		]
			
