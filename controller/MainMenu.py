#!/usr/bin/python
#
# MainMenu.py - the main menu
#
# (c) David Haworth

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

	def Item(self, i):
		return self.items[i]

	def Action(self, i):
		return self.actions[i]
