#!/usr/bin/python
import os

base = "/data/audio/jukebox/00-Artist"

current = base
working = True

while working:
	print "current = "+current
	files = os.listdir(current)
	index = 1
	for f in sorted(files):
		print str(index)+" : "+f
		index = index + 1

	print "u : up a level"
	print "q : quit"

	sel = raw_input("--> ")
	input_ok = False
	while not input_ok:
		if sel == "q":
			input_ok = True
			working = False
		elif sel == "u":
			input_ok = True
			# ToDo - go up a level
		else:
			try:
				index = int(sel)
				input_ok = True
				# ToDo - process the file/directory
			except:
				sel = raw_input("Try again --> ")
