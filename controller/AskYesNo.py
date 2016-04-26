#!/usr/bin/python
#
# AskYesNo.py - a message screen of up to 2 lines with Yes and No
#
# (c) David Haworth

from Menu import Menu, MenuThing

class AskYesNo(Menu):
	def __init__(self, mh, lcd, m):
		Menu.__init__(self, mh, lcd)

		self.things.append(MenuThing(m[0],	self.Nix,	''))

		if len(m) > 1:
			self.things.append(MenuThing(m[1],	self.Nix,	''))
		else:
			self.things.append(MenuThing('',	self.Nix,	''))

		self.things.append(MenuThing('Yes',	self.Answer,	'ans.yes'))
		self.things.append(MenuThing('No',	self.Answer,	'ans.no'))

		self.min_current = 2
		self.current = 3

	def Nix(self, mt, evt):
		return False

	def Answer(self, mt, evt):
		if evt == 'ok':
			self.mh.Answer(mt.data)
			return True
		return False
