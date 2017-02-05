#!/bin/sh
#
# Script to bring up ethernet LAN.
#
# Run as root!

# Bring down any existing WiFi link
ifconfig wlan0 down
killall wpa_supplicant
dhclient -r wlan0

# Bring up the ethernet interface with defaults
ifconfig eth0 up
