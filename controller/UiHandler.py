#!/usr/bin/python
#
# UiHandler.py - handler for the RadioPi user interface
#
# (c) David Haworth

from LcdHandler import LcdHandler
from MainMenu import MainMenu
from Browser import Browser
from MountMenu import MountMenu
from MessageScreen import MessageScreen
from AskYesNo import AskYesNo

# UI modes
mode_Disconnected = 0
mode_StartupWait = 1
mode_Startup = 2
mode_Home = 3
mode_Menu = 4

# Home screen positions
row_artist	= 1
col_artist	= 1
row_album	= 2
col_album	= 1
row_title	= 3
col_title	= 1
row_time	= 4
col_time	= 1
row_dur		= 4
col_dur		= 6
row_vol		= 4
col_vol		= 18	# 3 digits


class UiHandler:
	def __init__(self, mpd):
		self.mpd = mpd						# MPD handler
		self.mode = mode_Disconnected		# Current mode
		self.count = 0
#----
		self.vol = -1						# State of info on screen. Only update if changed.
		self.time = -1
		self.artist = ''
		self.album = ''
		self.title = ''
		self.dur = -1
		self.state = ''
		self.force = True					# Forced update
#----
		self.menu = None
		self.menustack = []
		self.lcd = LcdHandler()
		if self.lcd.Open():
			self.mode = mode_StartupWait
			self.count = 2

#===========================================================
# Enter the menu system
#===========================================================
	def Enter(self):
		self.menustack = []							# Clear out existing menus (if any)
		self.menu = MainMenu(self, self.lcd)		# Create the main menu.
		self.menu.Show()

#===========================================================
# Enter the music browser at the specified place.
#===========================================================
	def EnterBrowser(self, dir):
		self.menustack.append(self.menu)			# Push current menu.
		self.menu = Browser(self, self.lcd, dir)	# Create a browser.
		self.menu.Show()

#===========================================================
# Enter the mount menu.
#===========================================================
	def EnterMountMenu(self):
		self.menustack.append(self.menu)			# Push current menu.
		self.menu = MountMenu(self, self.lcd)		# Create the menu.
		self.menu.Show()

#===========================================================
# Show a message.
#===========================================================
	def ShowMessage(self, m, ack):
		self.menustack.append(self.menu)					# Push current menu.
		self.menu = MessageScreen(self, self.lcd, m, ack)	# Create the message screen.
		self.menu.Show()

#===========================================================
# Ask a question
#===========================================================
	def AskYesNo(self, m):
		self.menustack.append(self.menu)			# Push current menu.
		self.menu = AskYesNo(self, self.lcd, m)		# Create the yes/no screen.
		self.menu.Show()

#===========================================================
# Receive the answer from AskYesNo
#===========================================================
	def Answer(self, ans):
		if len(self.menustack) == 0:
			self.menu = None
			self.ModeHome()
		else:
			self.menu = self.menustack.pop()
			self.menu.Event(ans)
			self.menu.Show()

#===========================================================
# Go back up a level.
#===========================================================
	def Back(self):
		if len(self.menustack) == 0:
			self.menu = None
			self.ModeHome()
		else:
			self.menu = self.menustack.pop()
			self.menu.Show()

#===========================================================
# Handle a timer event
#===========================================================
	def Timer(self):
		if self.mode == mode_Disconnected:		# If disconnected, attempt to open
			if self.lcd.Open():
				self.mode = mode_StartupWait
				self.count = 2

		elif self.mode == mode_StartupWait:		# After successful open, let the terminal settle
			self.count -= 1
			if self.count <= 0:
				self.StartupScreen()
				self.mode = mode_Startup
				self.force = True
				self.count = 2

		elif self.mode == mode_Startup:			# Display splash screen.
			try:
				self.count -= 1
				if self.count <= 0:
					self.mode = mode_Home
					self.force = True
					self.HomeScreen()			# Redraw homw screen
			except:
				self.mode = mode_Disconnected

		elif self.mode == mode_Home:			# Update home screen
			try:
				self.HomeScreen()
			except:
				self.mode = mode_Disconnected

		else:									# After some inactivity, revert to home screen.
			self.count -= 1
			if self.count <= 0:
				self.count = 0
				self.mode = mode_Home
				self.force = True

		return False

#===========================================================
# Handle a user input event
#===========================================================
	def Event(self, evt):

		if self.mode < mode_Home:				# Ignore events during start sequence.
			return False

		self.count = 30							# Restart the inactivity timer

		if self.mode == mode_Home:				# On home screen, 'menu', 'ok' or 'right' enters menu.
			if evt == 'menu' or  evt == 'ok' or evt == 'right':
				self.mode = mode_Menu
				self.Enter()
				return True
			return False						# Ignore all other events while on home screen.

		if evt == 'home':						# Anywhere in the menus, 'home' exits back to the home screen
			self.menu = None					# Clear the menu stack
			self.menustack = []
			self.ModeHome()
			return True

		# Menu mode. Handle up/down/left/back as navigation on existing menu stack.
		if evt == 'back' or evt == 'left':
			self.Back()
			return True

		elif evt == 'up':
			self.menu.PtrUp()
			return True

		elif evt == 'down':
			self.menu.PtrDown()
			return True

		# All other events in menu mode: pass on to the individual menu
		return self.menu.Event(evt)


#===========================================================
# StartupScreen() - display startup screen
#===========================================================

	def StartupScreen(self):
		if self.force:
			self.lcd.HomeAndClear()
			self.lcd.Write('      RadioPi\r\n')
			self.lcd.Write('\r\n')
			self.lcd.Write('\r\n')
			self.lcd.Write('  waiting for mpd')
		self.force = False

#===========================================================
# ModeHome() - switch to 'home' mode (leave menu)
#===========================================================

	def ModeHome(self):
		self.mode = mode_Home
		self.force = True
		self.HomeScreen()

#===========================================================
# HomeScreen() - read mpd status and display it
#===========================================================

	def HomeScreen(self):
		l_artist = ''
		l_album = ''
		l_title = ''
		l_dur = -1
		l_file = ''

		s = self.mpd.Status()
		l_vol = int(s['volume'])
		l_state = s['state']
		if l_state == 'stop':
			l_time = -1
		else:
			l_time = int(float(s['elapsed']))

		s = self.mpd.CurrentSong()
		if s:
			for k in s.keys():
				if k == 'artist':
					l_artist = s['artist']
				elif k == 'album':
					l_album = s['album']
				elif k == 'title':
					l_title = s['title']
				elif k == 'time':
					l_dur = int(s['time'])
				elif k == 'file':
					l_file = s['file']

			if l_title == '' and l_file != '':
				x, l_title = os.path.split(l_file)

		else:
			# No track
			l_artist = '      RadioPi'
			l_album = ''
			l_title = '===== no track ====='

		if self.force:
			self.lcd.HomeAndClear()

		if self.force or self.artist != l_artist:
			self.artist = l_artist
			self.lcd.WriteAt(row_artist, col_artist, self.artist)
			self.lcd.ClearEol()

		if self.force or self.album != l_album:
			self.album = l_album
			self.lcd.WriteAt(row_album, col_album, self.album)
			self.lcd.ClearEol()

		if self.force or self.title != l_title:
			self.title = l_title
			self.lcd.WriteAt(row_title, col_title, self.title);
			self.lcd.ClearEol()

		if l_dur < 0:
			if self.force or self.dur != l_dur:
				self.dur = l_dur
				self.time = -1
				self.lcd.WriteAt(row_time, col_time, '           ')
		else:
			if self.force or self.time != l_time:
				self.time = l_time
				if l_time < 0:
					s_time = '--:--'
				else:
					mins = l_time / 60
					secs = l_time % 60
					s_time = '%02d:%02d'%(mins, secs)
				self.lcd.WriteAt(row_time, col_time, s_time)

			if self.force or self.dur != l_dur:
				self.dur = l_dur
				mins = l_dur / 60
				secs = l_dur % 60
				s_time = '/%02d:%02d'%(mins, secs)
				self.lcd.WriteAt(row_dur, col_dur, s_time)
		
		if self.force or self.vol != l_vol:
			self.vol = l_vol
			s_vol = '%3d'%(l_vol)
			self.lcd.WriteAt(row_vol, col_vol, s_vol)

		self.force = False

