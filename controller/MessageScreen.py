#!/usr/bin/python
#
# MessageScreen.py - a message screen of up to 3 lines with OK
#
# (c) David Haworth

from Menu import Menu, MenuThing

class MessageScreen(Menu):
	def __init__(self, mh, lcd, m):
		Menu.__init__(self, mh, lcd)

		self.things.append(MenuThing(m[0],	self.Nix,	''))

		if len(m) > 1:
			self.things.append(MenuThing(m[1],	self.Nix,	''))
		else:
			self.things.append(MenuThing('',	self.Nix,	''))

		if len(m) > 2:
			self.things.append(MenuThing(m[2],	self.Nix,	''))
		else:
			self.things.append(MenuThing('',	self.Nix,	''))

		self.things.append(MenuThing('OK',	self.Back,	''))
		self.min_current = 3
		self.current = 3

	def Nix(self, mt, evt):
		return False

	def Back(self, mt, evt):
		if evt == 'ok':
			self.mh.Back()
			return True
		return False
