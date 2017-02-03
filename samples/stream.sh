#!/bin/sh
mpc clear
mpc clearerror
mpc add "$1"
mpc play
