#!/bin/sh

cd /home/pi/RadioPi/controller

if [ "$1" = "start" ]; then
	./RadioPi.sh &
	exit 0
fi

sleep 5

while true; do
	if [ -f radiopi.log ]; then
		mv radiopi.log radiopi.log.o
	fi
	./RadioPi.py > radiopi.log 2>&1
done

