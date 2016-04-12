#!/usr/bin/python
#
# LcdHandler.py - handler for the display
#
# (c) David Haworth

import serial
from MpdHandler import MpdHandler
from MenuHandler import MenuHandler

# LCD config
lcd_dev = '/dev/ttyUSB0'
lcd_baud = 9600
lcd_nrows		= 4
lcd_ncols		= 20
lcd_go_artist	= "\033[1;1H"
lcd_go_album	= "\033[2;1H"
lcd_go_title	= "\033[3;1H"
lcd_go_time		= "\033[4;1H"
lcd_go_dur		= "\033[4;6H"		# 3 digits
lcd_go_vol		= "\033[4;18H"		# 3 digits
lcd_clreol		= "\033[0K"

# LCD modes
mode_Disconnected = 0
mode_StartupWait = 1
mode_Startup = 2
mode_Home = 3
mode_MainMenu = 4

class LcdHandler:
	def __init__(self, mpd):
		self.mpd = mpd
		self.menuhandler = MenuHandler(mpd, self)
		self.mode = mode_Disconnected			# Current mode
		self.vol = -1							# State of info on screen. Only update if changed.
		self.time = -1
		self.artist = ""
		self.album = ""
		self.title = ""
		self.dur = -1
		self.state = ""
		self.force = True						# Forced update
		self.Open()

#===========================================================
# Open() - attempt to open the LCD
#===========================================================
	# After successfully opening the port (which resets the terminal) we need to wait a while to allow
	# the Arduino bootloader to settle.
	def Open(self):
		try:
			self.lcd = serial.Serial(lcd_dev, lcd_baud)
			self.mode = mode_StartupWait		# After successfully opening the port, allow a short time
			self.count = 2						# for the Arduino bootloader to run.
		except:
			self.mode = mode_Disconnected		# Failed; stay disconnected

#===========================================================
# Timer() - handle timer events
#===========================================================
	def Timer(self):
		if self.mode == mode_Disconnected:		# If disconnected, attempt to open
			self.Open()
		elif self.mode == mode_StartupWait:		# After successful open, let the terminal settle
			self.count -= 1
			if self.count <= 0:
				self.mode = mode_Startup
				self.force = True
		elif self.mode == mode_Startup:			# Display splash screen.
			try:
				self.StartupScreen()
				self.count -= 1
				if self.count <= 0:
					self.mode = mode_Home
					self.force = True
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
				self.mode = mode_Home
				self.force = True
		return False

#===========================================================
# Event() - handle user input events
#===========================================================
	def Event(self, evt):
		if self.mode < mode_Home:				# Ignore events during start sequence.
			return False

		if self.mode == mode_Home:				# On home screen, 'menu' enters menu.
			if evt == 'menu':
				self.mode = mode_MainMenu
				self.menuhandler.Enter()
				return True
			return False						# Ignore everything else on home screen.

		if evt == 'home':						# Anywhere in the menus, 'home' exits back to the home screen
			self.mode = mode_Home
			self.force = True
			return True

		return self.menuhandler.Event(evt)

#===========================================================
# StartupScreen() - display startup screen
#===========================================================

	def StartupScreen(self):
		if self.force:
			self.lcd.write("\f")
			#              "                    "
			self.lcd.write("      RadioPi\r\n")
			self.lcd.write("\r\n")
			self.lcd.write("\r\n")
			self.lcd.write("  waiting for mpd")
	
		self.force = False

#===========================================================
# HomeScreen() - read mpd status and display it
#===========================================================

	def HomeScreen(self):
		l_artist = ""
		l_album = ""
		l_title = ""
		l_dur = -1
		l_file = ""

		s = self.mpd.Status()
		l_vol = int(s['volume'])
		l_state = s['state']
		if l_state == "stop":
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

			if l_title == "" and l_file != "":
				x, l_title = os.path.split(l_file)

		else:
			# No track
			l_artist = "      RadioPi"
			l_album = ""
			l_title = "===== no track ====="

		if self.force:
			self.lcd.write("\f")

		if self.force or self.artist != l_artist:
			self.artist = l_artist
			self.lcd.write(lcd_go_artist)
			self.lcd.write(self.artist);
			self.lcd.write(lcd_clreol)

		if self.force or self.album != l_album:
			self.album = l_album
			self.lcd.write(lcd_go_album)
			self.lcd.write(self.album);
			self.lcd.write(lcd_clreol)

		if self.force or self.title != l_title:
			self.title = l_title
			self.lcd.write(lcd_go_title)
			self.lcd.write(self.title);
			self.lcd.write(lcd_clreol)

		if l_dur < 0:
			if self.force or self.dur != l_dur:
				self.dur = l_dur
				self.time = -1
				self.lcd.write(lcd_go_time)
				self.lcd.write("           ")
		else:
			if self.force or self.time != l_time:
				self.time = l_time
				if l_time < 0:
					s_time = "--:--"
				else:
					mins = l_time / 60
					secs = l_time % 60
					s_time = "%02d:%02d"%(mins, secs)
				self.lcd.write(lcd_go_time)
				self.lcd.write(s_time)

			if self.force or self.dur != l_dur:
				self.dur = l_dur
				mins = l_dur / 60
				secs = l_dur % 60
				s_time = "/%02d:%02d"%(mins, secs)
				self.lcd.write(lcd_go_dur)
				self.lcd.write(s_time)
		
		if self.force or self.vol != l_vol:
			self.vol = l_vol
			s_vol = "%3d"%(l_vol)
			self.lcd.write(lcd_go_vol)
			self.lcd.write(s_vol)

		self.force = False

	def GetNRows(self):
		return lcd_nrows

	def HomeAndClear(self):
		self.lcd.write('\f')

	def NewLine(self):
		self.lcd.write('\r\n')

	def Write(self, str):
		self.lcd.write(str)

	def GoStr(self, row, col):
		return '\033[' + str(row) + ';' + str(col) + 'H'
