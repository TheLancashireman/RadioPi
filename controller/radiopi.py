#!/usr/bin/python
#
# Headless control program for RadioPi

import RPi.GPIO as GPIO
import time
from mpd import MPDClient
import serial

# Open port to LCD terminal (fixme: need to specify or discover)
lcd = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(5)
lcd.write("\f")
time.sleep(5)
lcd.write("Starting ...")
time.sleep(5)

# Open connection to mpd
mpdc = MPDClient()
mpdc.timeout = 10
mpdc.idletimeout = None
mpdc.connect("localhost", 6600)

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
mode_Home = 1
mode = mode_Home

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

lcd_go_artist	= "\033[1;1H"
lcd_go_album	= "\033[2;1H"
lcd_go_title	= "\033[3;1H"
lcd_go_time		= "\033[4;1H"
lcd_go_vol		= "\033[4;18H"		# 3 digits
lcd_clreol		= "\033[0K"

def HomeScreen():
	global g_vol
	global g_time
	global g_artist
	global g_album
	global g_title

	mpdstatus = mpdc.status()
	l_vol = int(mpdstatus['volume'])
	l_time = int(float(mpdstatus['elapsed']))
	mpdsong = mpdc.currentsong()
	l_artist = mpdsong['artist']
	l_album = mpdsong['album']
	l_title = mpdsong['title']

	if ( g_artist != l_artist ):
		g_artist = l_artist
		lcd.write(lcd_go_artist)
		lcd.write(g_artist);
		lcd.write(lcd_clreol)

	if ( g_album != l_album ):
		g_album = l_album
		lcd.write(lcd_go_album)
		lcd.write(g_album);
		lcd.write(lcd_clreol)

	if ( g_title != l_title ):
		g_title = l_title
		lcd.write(lcd_go_title)
		lcd.write(g_title);
		lcd.write(lcd_clreol)

	if ( g_time != l_time ):
		g_time = l_time
		mins = l_time / 60
		secs = l_time % 60
		s_time = "%02d:%02d"%(mins, secs)
		lcd.write(lcd_go_time)
		lcd.write(s_time)
		
	if ( g_vol != l_vol ):
		g_vol = l_vol
		s_vol = "%3d"%(l_vol)
		lcd.write(lcd_go_vol)
		lcd.write(s_vol)

#=======================================
#GPIO.add_event_detect(encoderA, GPIO.BOTH, callback=edgeA, bouncetime=10)
#GPIO.add_event_detect(encoderB, GPIO.BOTH, callback=edgeB, bouncetime=10)

try:
	while 1:
		time.sleep(1)
		if ( mode == mode_Home ):
			HomeScreen()
except KeyboardInterrupt:		# If CTRL+C is pressed, exit cleanly:
	# GPIO.cleanup() # cleanup all GPIO
	print ""
