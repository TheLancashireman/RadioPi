#!/usr/bin/python
#
# Config.py - configuration for RadioPi
#
# (c) David Haworth

class Config:
	def __init__(self):
		self.music_dir		= '/home/pi/Music'	# Base of music directory
		self.music_ext		= 'external'		# Mount point for external filesystems (subdir of music_dir)
		self.music_sfx		= set([".ogg", ".mp3", ".wav", ".flac"])
		self.menu_cursor	= '\x7e'			# A right-pointing arrow; used as 'current' pointer on menu display
		self.ack_cursor		= '\xdb'			# A square; used as a transient 'done' indicator on menu
		self.dbg_level		= 1

radiopi_cfg = Config()
