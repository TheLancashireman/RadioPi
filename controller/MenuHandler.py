#!/usr/bin/python
#
# MenuHandler.py - handler for the display
#
# (c) David Haworth

from MainMenu import MainMenu
from Browser import Browser

class MenuHandler:
	def __init__(self, mpd, lcd):
		self.mpd = mpd				# MPD handler
		self.lcd = lcd				# Display handler
		self.menu = None
		self.menustack = []

	# Enter the menu system
	def Enter(self):
		self.menustack = []							# Clear out existing menus (if any)
		self.menu = MainMenu(self, self.lcd)		# Create the main menu.
		self.menu.Show()

	# Enter the music browser at the specified place.
	def EnterBrowser(self, dir):
		self.menustack.append(self.menu)			# Push current menu.
		self.menu = Browser(self, self.lcd, dir)	# Create a browser.
		self.menu.Show()

	# Go back up a level.
	def Back(self):
		self.menu = self.menustack.pop()
		self.menu.Show()

	def Event(self, evt):
		result = False
		if evt == 'home':
			self.menu = None
			self.menustack = []
			result = True
		elif evt == 'back' or evt == 'left':
			self.Back()
			result = True
		elif evt == 'up':
			self.menu.PtrUp()
			result = True
		elif evt == 'down':
			self.menu.PtrDown()
			result = True
		else:
			result = self.menu.Event(evt)
