#!/usr/bin/python
#
# MenuThing.py - a thing on a menu
#
#	text - the text to display
#	data - the payload for the action
#   action - what to do when the menu is selected
#
# (c) David Haworth

class MenuThing:
	def __init__(self, t, a, d):
		self.text = t
		self.action = a
		self.data = d
