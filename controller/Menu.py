#!/usr/bin/python
#
# Menu.py - an abstract menu with things on it
#
# (c) David Haworth
from Config import Config
from RadioPiLib import Dbg_Print

# MenuThing.py - a thing on a menu
#
#	text - the text to display
#	data - the payload for the action
#   action - what to do when the menu is selected
class MenuThing:
	def __init__(self, t, a, d):
		self.text = t
		self.action = a
		self.data = d

class Menu:
	def __init__(self, ui, lcd, eq):
		cfg = Config()
		self.ui = ui
		self.lcd = lcd
		self.eq = eq
		self.cursor = cfg.menu_cursor
		self.ack_cursor = cfg.ack_cursor
		self.top = 0			# First visible thing
		self.current = 0		# Current position of pointer
		self.min_current = 0	# Lowest index of pointer - nonzero for dialogs.
		self.things = []

	def Back(self, mt, evt):
		if evt == 'ok':
			self.ui.Back()
			return True
		return False

	def Show(self):
		nrows = self.lcd.GetNRows()
		j = self.top
		for i in range(nrows):
			if i == 0:
				self.lcd.HomeAndClear()
			else:
				self.lcd.NewLine()
			if j < len(self.things):
				self.lcd.Write(' ' + self.things[j].text)
			j += 1
		if self.current >= self.top and self.current < (self.top + nrows):
			l = self.current - self.top + 1
			self.lcd.Write(self.lcd.GoStr(l, 1) + self.cursor + '\r')

	def PtrUp(self):
		if self.current > self.min_current:
			self.current -= 1
			if self.current < self.top:
				self.top = self.current
				self.Show()
			else:
				l = self.current - self.top + 1
				self.lcd.Write('\r ' + self.lcd.GoStr(l, 1) + self.cursor + '\r')

	def PtrDown(self):
		max = len(self.things)-1
		if self.current < max:
			Dbg_Print(5, 'PtrDown', max, self.current)
			self.current += 1
			if self.current < self.top+self.lcd.GetNRows():
				self.lcd.Write('\r \r\n' + self.cursor + '\r')
			else:
				self.lcd.Write('\r \r\n' + self.cursor + self.things[self.current].text + '\r')
				self.top += 1

	def Goto(self, tenth):
		self.current = int((len(self.things) * tenth)/10)
		self.top = self.current - 1
		if self.top < 0:
			self.top = 0
		self.Show()

	def Ack(self):
		self.lcd.Write('\r' + self.ack_cursor + '\r')

	def Event(self, evt):
		r = True
		if evt == 'up':
			self.PtrUp()
		elif evt == 'down':
			self.PtrDown()
		elif evt in ['0','1','2','3','4','5','6','7','8','9']:
			self.Goto(int(evt))
		else:
			th = self.things[self.current]
			r = th.action(th, evt)
		return r
