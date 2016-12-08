#!/bin/sh

export REQUEST_METHOD="GET"
export QUERY_STRING="restartmpd"
export SCRIPT_NAME="webradiopi.py"
export DOCUMENT_ROOT="/var/www/html"

./webradiopi.py
