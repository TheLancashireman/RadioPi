#!/usr/bin/python
#
# Headless control program for RadioPi

import RPi.GPIO as GPIO
import time
import mpd
from mpd import MPDClient
import serial
import os
import sys

# Open port to LCD terminal (fixme: need to specify or discover)
lcd = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)
lcd.write("\fRadioPi starting ...")

# Open connection to mpd
mpdc = MPDClient()
mpdc.timeout = 10
mpdc.idletimeout = None
mpdc.connect("localhost", 6600)

mpdConnected = True
mpdLock = False

# Initialise GPIO for the rotary encoder
encoderA = 23		# BCM no. of Encoder 'A'
encoderB = 24		# BCM no. of Encoder 'B'
encoderD = 25		# BCM no. of Encoder 'D' (switch)

GPIO.setmode(GPIO.BCM)
GPIO.setup(encoderA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderB, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(encoderD, GPIO.IN, pull_up_down=GPIO.PUD_UP)

stateB = False
countBase = 1000000
countRaw = countBase

# Initialise controller state
mode_Startup = 1
mode_Home = 2
mode_Menu = 3
mode = mode_Startup

g_vol = -1
g_time = -1
g_artist = ""
g_album = ""
g_title = ""
g_dur = -1
g_state = ""
g_force = True

lcd_nrows		= 4
lcd_ncols		= 20
lcd_go_artist	= "\033[1;1H"
lcd_go_album	= "\033[2;1H"
lcd_go_title	= "\033[3;1H"
lcd_go_time		= "\033[4;1H"
lcd_go_dur		= "\033[4;6H"		# 3 digits
lcd_go_vol		= "\033[4;18H"		# 3 digits
lcd_clreol		= "\033[0K"

main_menu = [
	"Clear playlist",
	"Add tracks",
	"Manage playlist",
	"MPD options",
	"Foo",
	"Bar",
	"Quxx"
]

menu_Main = 1		# Constant - menu identifier
menu_no = menu_Main	# Current menu
menu = main_menu	# Current menu
menu_pos = 0		# Position in menu
menu_top = 0		# Position of menu on screen (the item that's on the top line of the display)

#===========================================================
# EdgeA() - Callback for edge on channel A
#===========================================================
def edgeA(channel):
	global countRaw
	global countMax
	global countMin
	global stateB

	stateA = GPIO.input(encoderA)
	stateB = GPIO.input(encoderB)
	if stateA == stateB:
		# Increase
		countRaw += 1
	else:
		# Decrease
		countRaw -= 1

#===========================================================
# Callback for edge on channel B  (not used)
#===========================================================
def edgeB(channel):
	global stateB
	stateB = GPIO.input(encoderB)


#===========================================================
# Callback for edge on channel D
#===========================================================
def edgeD(channel):
	return


#===========================================================
# HomeScreen() - read mpd status and display it
#===========================================================

def HomeScreen():
	global g_vol
	global g_time
	global g_artist
	global g_album
	global g_title
	global g_dur
	global g_force
	global mpdLock

	l_artist = ""
	l_album = ""
	l_title = ""
	l_dur = -1
	l_file = ""
	mpdLock = True

	mpdstatus = mpdc.status()
	l_vol = int(mpdstatus['volume'])
	state = mpdstatus['state']
	if state == "stop":
		l_time = -1
	else:
		l_time = int(float(mpdstatus['elapsed']))

	mpdsong = mpdc.currentsong()
	if mpdsong:
		for k in mpdsong.keys():
			if k == 'artist':
				l_artist = mpdsong['artist']
			elif k == 'album':
				l_album = mpdsong['album']
			elif k == 'title':
				l_title = mpdsong['title']
			elif k == 'time':
				l_dur = int(mpdsong['time'])
			elif k == 'file':
				l_file = mpdsong['file']

		if l_title == "" and l_file != "":
			x, l_title = os.path.split(l_file)

	else:
		# No track
		l_artist = "      RadioPi"
		l_album = ""
		l_title = "===== no track ====="

	if g_force:
		lcd.write("\f")

	if g_force or g_artist != l_artist:
		g_artist = l_artist
		lcd.write(lcd_go_artist)
		lcd.write(g_artist);
		lcd.write(lcd_clreol)

	if g_force or g_album != l_album:
		g_album = l_album
		lcd.write(lcd_go_album)
		lcd.write(g_album);
		lcd.write(lcd_clreol)

	if g_force or g_title != l_title:
		g_title = l_title
		lcd.write(lcd_go_title)
		lcd.write(g_title);
		lcd.write(lcd_clreol)

	if l_dur < 0:
		if g_force or g_dur != l_dur:
			g_dur = l_dur
			g_time = -1
			lcd.write(lcd_go_time)
			lcd.write("           ")
	else:
		if g_force or g_time != l_time:
			g_time = l_time
			if l_time < 0:
				s_time = "--:--"
			else:
				mins = l_time / 60
				secs = l_time % 60
				s_time = "%02d:%02d"%(mins, secs)
			lcd.write(lcd_go_time)
			lcd.write(s_time)

		if g_force or g_dur != l_dur:
			g_dur = l_dur
			mins = l_dur / 60
			secs = l_dur % 60
			s_time = "/%02d:%02d"%(mins, secs)
			lcd.write(lcd_go_dur)
			lcd.write(s_time)
		
	if g_force or g_vol != l_vol:
		g_vol = l_vol
		s_vol = "%3d"%(l_vol)
		lcd.write(lcd_go_vol)
		lcd.write(s_vol)

	mpdLock = False
	g_force = False

#===========================================================
# StartupScreen() - display startup screen
#===========================================================

def StartupScreen():
	global g_force

	if g_force:
		lcd.write("\f")
		#         "                    "
		lcd.write("      RadioPi\r\n")
		lcd.write("\r\n")
		lcd.write("\r\n")
		lcd.write("  waiting for mpd")

	g_force = False

#===========================================================
# ChangeVolume() - adjust the volume
#===========================================================

def ChangeVolume(diff):
	global g_vol

	g_vol += diff
	if g_vol < 0:
		g_vol = 0
	elif g_vol > 100:
		g_vol = 100
	mpdc.setvol(str(g_vol))
	lcd.write(lcd_go_vol)
	lcd.write("%3d"%(g_vol))

#===========================================================
# PlayOrPause() - if stopped, play. Otherwise toggle pause
#===========================================================

def PlayOrPause():
	mpdstatus = mpdc.status()
	state = mpdstatus['state']
	if state == "stop":
		mpdc.play()
	else:
		mpdc.pause()

#===========================================================
# PressDetect() - detect button press
#===========================================================

btnCount = 0

def PressDetect():
	global btnCount

	stateD = GPIO.input(encoderD)
	result = 0

	if stateD:
		# Button not pressed
		if btnCount > 50:
			result = 2		# Long press
		elif btnCount > 5:
			result = 1		# Short press
		btnCount = 0
	else:
		# Button pressed
		btnCount += 1

	return result

#===========================================================
# Menu_Show() - show a menu
#===========================================================
def Menu_Show(menu, top, pos):
	global lcd_nrows

	for i in range(lcd_nrows):
		if i == 0:
			lcd.write("\f")
		else:
			lcd.write("\r\n")
		lcd.write(" "+menu[top+i])
	if pos >= top and pos < (top+lcd_nrows):
		line = pos - top + 1
		lcd.write("\033["+str(line)+";1H\x7e\r")

#===========================================================
# Menu_Start() - enter the menu
#===========================================================
def Menu_Start():
	global mode_Menu
	global menu_Main
	global main_menu
	global mode
	global menu
	global menu_pos
	global menu_top

	print "Menu_Start()"
	mode = mode_Menu
	menu_no = menu_Main
	menu = main_menu
	menu_pos = 0
	menu_top = 0
	Menu_Show(main_menu, 0, 0)

#===========================================================
# Menu_UpDown() - scroll through the menu
#===========================================================
def Menu_UpDown(count):
	global menu
	global menu_pos
	global menu_top
	global lcd_nrows

	print "Menu_UpDown()", count
	max = len(menu)-1

	if count > 0:
		if menu_pos < max:
			menu_pos += 1
			if menu_pos < menu_top+lcd_nrows:
				lcd.write("\r \r\n\x7e\r")
			else:
				lcd.write("\r \r\n\x7e"+menu[menu_pos])
				menu_top += 1
	elif count < 0:
		if menu_pos > 0:
			menu_pos -= 1
			if menu_pos < menu_top:
				lcd.write("\r \r\v\x7e"+menu[menu_pos])
				menu_top -= 1
			else:
				lcd.write("\r \r\v\x7e\r")

#===========================================================
# Menu_Press() - button press on menu
#===========================================================
def Menu_Press(p):
	print "Menu_Press()", p

#===========================================================
# Home_UpDown() - handle turns on the home screen
#===========================================================
def Home_UpDown(count):
	global g_vol
	if g_vol >= 0:
		ChangeVolume(count)

#===========================================================
# Home_Press() - button press on home screen
#===========================================================
def Home_Press(p):
	if p == 1:
		PlayOrPause()
	elif p == 2:
		Menu_Start()
		

#=======================================

GPIO.add_event_detect(encoderA, GPIO.BOTH, callback=edgeA, bouncetime=10)
#GPIO.add_event_detect(encoderB, GPIO.BOTH, callback=edgeB, bouncetime=100)

StartupScreen()
mode = mode_Home
g_force = True

oneSecCount = 0

try:
	while 1:
		try:
			time.sleep(0.01)

			# Detect and handle dial rotation
			if countRaw != countBase:
				diff = (countRaw - countBase)
				countRaw = countBase
				if mode == mode_Home:
					Home_UpDown(diff)
				elif mode == mode_Menu:
					Menu_UpDown(diff)

			# Detect and handle dial press
			x = PressDetect()
			if x > 0:
				if mode == mode_Home:
					Home_Press(x)
				elif mode == mode_Menu:
					Menu_Press(x)

			# Regular update activity
			oneSecCount += 1
			if oneSecCount >= 100:
				oneSecCount = 0
				if not mpdConnected:
					mpdc.connect("localhost", 6600)
					mpdConnected = True
					mode = mode_Home
					g_force = True
				if mode == mode_Startup:
					StartupScreen()
				elif mode == mode_Home:
					HomeScreen()

		except mpd.ConnectionError:
			mpdConnected = False
			mode = mode_Startup
			g_force = True

except KeyboardInterrupt:		# CTRL-C pressed
	print ""

GPIO.cleanup() # cleanup all GPIO
mpdc.close()

