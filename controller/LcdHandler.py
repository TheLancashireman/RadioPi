#!/usr/bin/python
#
# LcdHandler.py - handler for the display
#
# (c) David Haworth

import serial

# LCD config
lcd_dev		= '/dev/ttyUSB'
lcd_baud	= 9600
lcd_nrows	= 4
lcd_ncols	= 20
lcd_clreol	= "\033[0K"

class LcdHandler:
	def __init__(self):
		self.lcd = None
		self.connected = False

#===========================================================
# Attempt to open the LCD
# After successfully opening the port (which resets the terminal) we need to wait a while to allow
# the Arduino bootloader to settle.
# ToDo: what if the device connects on ttyUSB1...?
#===========================================================
	def Open(self):
		for n in range(9):
			try:
				self.lcd = serial.Serial(lcd_dev+str(n), lcd_baud)
				self.connected = True
				return self.connected
			except:
				self.connected = False
		return self.connected

#===========================================================
# Return the number of rows on the screen
#===========================================================
	def GetNRows(self):
		return lcd_nrows

#===========================================================
# Cursor to top left, clear screen
#===========================================================
	def HomeAndClear(self):
		self.lcd.write('\f')

#===========================================================
# Go to start of next line (scrolls up if at bottom)
#===========================================================
	def NewLine(self):
		self.lcd.write('\r\n')

#===========================================================
# Clear to end of line
#===========================================================
	def ClearEol(self):
		self.lcd.write(lcd_clreol)

#===========================================================
# Write a string to the display
#===========================================================
	def Write(self, str):
		self.lcd.write(str)

#===========================================================
# Go to specified position
#===========================================================
	def GoStr(self, row, col):
		return '\033[' + str(row) + ';' + str(col) + 'H'

#===========================================================
# Go to specified position and write
#===========================================================
	def WriteAt(self, row, col, str):
		self.lcd.write(self.GoStr(row, col) + str)
