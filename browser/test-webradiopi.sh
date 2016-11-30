#!/bin/sh

export REQUEST_METHOD="GET"
export QUERY_STRING="browse&00-Artist"
export SCRIPT_NAME="webradiopi.py"
export DOCUMENT_ROOT="/data/mirror/thelancashireman.org/"

./webradiopi.py
