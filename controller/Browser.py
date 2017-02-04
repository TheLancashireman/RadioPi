#!/usr/bin/python
#
# Browser.py - a browser menu for a given directory
#
# (c) David Haworth

from Menu import Menu, MenuThing
from Config import radiopi_cfg
import os

class Browser(Menu):
	def __init__(self, ui, lcd, eq, dir):
		Menu.__init__(self, ui, lcd, eq)
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
		(n,e) = os.path.splitext(f.lower())
		return os.path.isfile(f) and e in radiopi_cfg.music_sfx

	# Add all the playable files in the MenuThing's directory
	def AddAll(self, mt, evt):
		if evt == 'ok':
			self.eq.PutEvent("add " + mt.data)
			self.Ack()
			return True
		return False

	def DirAction(self, mt, evt):
		if evt == 'red':
			return self.AddAll(mt, 'ok')
		elif evt == 'ok' or evt == 'right':
			self.ui.EnterBrowser(mt.data)
			return True
		return False

	def FileAction(self, mt, evt):
		if evt == 'ok':
			self.eq.PutEvent("add " + mt.data)
			self.Ack()
			return True
		return False
