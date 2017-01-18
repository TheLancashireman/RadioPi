#!/usr/bin/python
import lirc

sockid = lirc.init("myprogram")

while True:
	print lirc.nextcode()
