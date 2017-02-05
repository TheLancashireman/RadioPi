#!/bin/sh
#
# Script to bring up wireless LAN. Parameter $1 is the wpa_supplicant-SSID.conf file
#
# Run as root!

# Bring down ethernet link
ifconfig eth0 down

# Bring down any existing WiFi link
ifconfig wlan0 down
killall wpa_supplicant
dhclient -r wlan0

# Bring up the WiFi with the specified wpa_supplicant config file
ifconfig wlan0 up
wpa_supplicant -Dnl80211 -iwlan0 -c/etc/wpa_supplicant/${1} -B
dhclient wlan0
