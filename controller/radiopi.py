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

# Initialise GPIO for the rotary encoder
encoderA = 23       # BCM no. of Encoder 'A'
encoderB = 24       # BCM no. of Encoder 'B'

#GPIO.setmode(GPIO.BCM)
#GPIO.setup(encoderA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(encoderB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

stateB = False
scale = 1
countRaw = 0
countMax = 10*scale-1
countMin = 0

# Initialise controller state
mode_Startup = 1
mode_Home = 2
mode = mode_Startup

#===========================================================
# EdgeA() - Callback for edge on channel A
#===========================================================
def edgeA(channel):
	global countRaw
	global countMax
	global countMin
	global stateB
	stateA = GPIO.input(encoderA)
	if stateA == stateB:
		# Increase
		inc = 1
		if mode == mode_Home:
			if volume < 100:
				volume += 1
				mpdc.setvol(str(volume))
	else:
		# Decrease
		inc = -1
		if mode == mode_Home:
			if volume > 0:
				volume -= 1
				mpdc.setvol(str(volume))
	countRaw += inc
	if countRaw < countMin:
		countRaw = countMax
	if countRaw > countMax:
		countRaw = countMin

#===========================================================
# Callback for edge on channel B
#===========================================================
def edgeB(channel):
	global stateB
	stateB = GPIO.input(encoderB)


#===========================================================
# HomeScreen() - read mpd status and display it
#===========================================================

g_vol = -1
g_time = -1
g_artist = ""
g_album = ""
g_title = ""
g_dur = -1
g_state = ""
g_force = True

lcd_go_artist	= "\033[1;1H"
lcd_go_album	= "\033[2;1H"
lcd_go_title	= "\033[3;1H"
lcd_go_time		= "\033[4;1H"
lcd_go_dur		= "\033[4;6H"		# 3 digits
lcd_go_vol		= "\033[4;18H"		# 3 digits
lcd_clreol		= "\033[0K"

def HomeScreen():
	global g_vol
	global g_time
	global g_artist
	global g_album
	global g_title
	global g_dur
	global g_force

	l_artist = ""
	l_album = ""
	l_title = ""
	l_dur = -1
	l_file = ""

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

#=======================================
#GPIO.add_event_detect(encoderA, GPIO.BOTH, callback=edgeA, bouncetime=10)
#GPIO.add_event_detect(encoderB, GPIO.BOTH, callback=edgeB, bouncetime=10)

StartupScreen()
mode = mode_Home
g_force = True

try:
	while 1:
		try:
			time.sleep(1)
			if mode == mode_Startup:
				StartupScreen()
			if mode == mode_Home:
				HomeScreen()
			if not mpdConnected:
				mpdc.connect("localhost", 6600)
				mpdConnected = True
				mode = mode_Home
				g_force = True
		except mpd.ConnectionError:
			mpdConnected = False
			mode = mode_Startup
			g_force = True

except KeyboardInterrupt:		# CTRL-C pressed
	print ""

# GPIO.cleanup() # cleanup all GPIO
mpdc.close()

