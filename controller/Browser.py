#!/usr/bin/python
#
# Browser.py - a browser menu for a given directory
#
# (c) David Haworth

from Menu import Menu, MenuThing
import os

class Browser(Menu):
	def __init__(self, mh, lcd, dir):
		Menu.__init__(self, mh, lcd)
		self.things.append(MenuThing('Add all',	self.AddAll,	dir))	# Might get removed later
		self.things.append(MenuThing('Back',	self.Back,		''))

		files = os.listdir(dir)
		files.sort()

		# Add directories first
		for f in files:
			ff = os.path.join(dir, f)
			if os.path.isdir(ff):
				self.things.append(MenuThing(f,	self.DirAction,	ff))

		# Add playable files. Ignore all others
		nPlayable = 0
		for f in files:
			ff = os.path.join(dir, f)
			if self.IsPlayable(ff):
				nPlayable += 1
				self.things.append(MenuThing(f,	self.FileAction, ff))

		# If there are no playable files, remove the Add All option.
		if nPlayable == 0:
			self.things.pop(0)

	# MPD appears to trigger an exception for non-playable files (CommandError) so for
	# the moment we only check if it's a file.
	# WARNING: the add command claims to be recursive for directories, but appears not to work.
	def IsPlayable(self, f):
		return os.path.isfile(f)

	# Add all the playable files in the MenuThing's directory
	def AddAll(self, mt, evt):
		if evt == 'ok':
			dir = mt.data
			files = os.listdir(mt.data)
			files.sort()
			for f in files:
				ff = os.path.join(dir, f)
				if self.IsPlayable(ff):
					self.mh.mpd.Add('file://'+ff)
			return True
		return False

	def Back(self, mt, evt):
		if evt == 'ok':
			self.mh.Back()
			return True
		return False

	def DirAction(self, mt, evt):
		if evt == 'ok':
			return self.AddAll(mt, evt)
		elif evt == 'right':
			self.mh.EnterBrowser(mt.data)
			return True
		return False

	def FileAction(self, mt, evt):
		if evt == 'ok':
			self.mh.mpd.Add('file://'+mt.data)
			return True
		return False
