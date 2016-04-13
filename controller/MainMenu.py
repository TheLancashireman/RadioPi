#!/usr/bin/python
#
# MainMenu.py - the main menu
#
# (c) David Haworth
from MenuThing import MenuThing

class MainMenu:
	def __init__(self, mh):
		self.top = 0		# First visible thing
		self.ptrpos = 0		# Current position of pointer
		self.things = []
		self.things.append('Clear playlist',	mh.ClearPlaylist,	'')
		self.things.append('Add to playlist',	mh.AddTracks,		'')
		self.things.append('Manage playlist',	mh.ManagePlaylist,	'')
		self.things.append('Mount external',	mh.MountExternal,	'')
		self.things.append('Umount external',	mh.UmountExternal,	'')
		self.things.append('MPD options',		mh.MpdOptions,		'')
