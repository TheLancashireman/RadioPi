#!/usr/bin/python

import os

basedir = "/data/audio/jukebox/00-Artist"

content = sorted(os.listdir(basedir))

for x in content:
	print x

