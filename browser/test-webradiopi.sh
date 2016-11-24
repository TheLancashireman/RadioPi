#!/bin/sh

export REQUEST_METHOD="GET"
export QUERY_STRING="browse&"
export SCRIPT_NAME="webradiopi.py"
export DOCUMENT_ROOT="/data/mirror/thelancashireman.org/"

./webradiopi.py
