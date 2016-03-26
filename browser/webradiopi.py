#!/usr/bin/python
import os

music_dir = "/data/audio/jukebox"
music_ext = set([".ogg", ".mp3", ".wav", ".flac"])

###
# main() - top level function (gets called at the end)
###
def main():
	verify_env()
	process_request()
	return 0

###
# verify_env() - sanity checks on the CGI environment
###
def verify_env():

	# Make sure DOCUMENT_ROOT is set and specifies a directory
	try:
		docroot = os.environ["DOCUMENT_ROOT"]

		if not os.path.isdir(docroot):
			error_page(2002, "Server error - DOCUMENT_ROOT does not specify a directory.", "")
	except:
		error_page(2001, "Server error - DOCUMENT_ROOT is not defined.", "")


	# Make sure that the request method is GET. Error page if not!
	try:
		method = os.environ["REQUEST_METHOD"]

		if method != "GET":
			error_page(1001, "An unexpected REQUEST_METHOD ("+method+") was used with this script.", "")
	except:
		error_page(2003, "Server error - REQUEST_METHOD is not defined.", "")

	# Make sure the script name is defined. Error page if not!
	try:
		script_name = os.environ["SCRIPT_NAME"]
	except:
		error_page(2004, "Server error - SCRIPT_NAME is not defined.", "")

	# Make sure the query string is defined. Error page if not!
	try:
		query_string = os.environ["QUERY_STRING"]
	except:
		error_page(2005, "Server error - QUERY_STRING is not defined.", "")

###
# process_request() - process the query, decide what to do
###
def process_request():
	global music_dir

	query_string = os.environ["QUERY_STRING"].lower()

	if query_string == "":
		front_page()
	else:
		query_list = query_string.split('&')
		command = query_list[0]
		if command == "play":
			front_page()
		elif command == "pause":
			front_page()
		elif command == "stop":
			front_page()
		elif command == "next":
			front_page()
		elif command == "prev":
			front_page()
		elif command == "clear":
			front_page()
		elif command == "add":
			list_dir(music_dir)
		else:
			error_page(1002, "Unknown command "+command+"\n", webradiopi)

###
# front_page() - print the "home" page
###
def front_page():
	body = """
 <div>
  <ul id="controls">
   <li><a href="webradiopi.py?play">Play</a></li>
   <li><a href="webradiopi.py?pause">Pause</a></li>
   <li><a href="webradiopi.py?stop">Stop</a></li>
   <li><a href="webradiopi.py?next">Next</a></li>
   <li><a href="webradiopi.py?prev">Prev</a></li>
  </ul>
  <h2>Playlist</h2>
  <ul id="playlistcontrols">
   <li><a href="webradiopi.py?clear">Clear</a></li>
   <li><a href="webradiopi.py?add">Add</a></li>
  </ul>
 </div>
"""

	print_page("WebRadioPi", body, "webradiopi")

###
# list_dir() - create a page listing the contents of a specified directory
###
def list_dir(path):
	body = ""

	directories = []
	tracks = []

	files = os.listdir(path)
	n_tracks = 0
	n_dirs = 0
	for f in sorted(files):

		full = os.path.join(path, f)

		if os.path.isdir(full):		# Follows symlinks
			directories.append(f)
			n_dirs += 1
		elif os.path.isfile(full):	# Follows symlinks
			if istrack(f):
				tracks.append(f)
				n_tracks += 1
		# Ignore all other entries

	body += """
 <div>
  <h2>"""+path+"""</h2>
"""

	if  n_tracks > 0:
		body += "  <ul>\n"
		for i in range(n_tracks):
			body += "   <li>"+tracks[i]+"</li>\n"
		body += "  </ul>\n"
	if  n_dirs > 0:
		if n_tracks > 0:
			body += "  <hr/>\n"
		body += "  <ul>\n"
		for i in range(n_dirs):
			body += "   <li>"+directories[i]+"</li>\n"
		body += "  </ul>\n"

	body += """
 </div>
"""
	print_page("WebRadioPi", body, "webradiopi")

###
# print_page() - prints the page; content type, doctype and the html head and body
###
def print_page(title, body_html, css):
	print """Content-type: text/html

<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">

<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
 <head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="" />
  <meta name="author" content="Dave" />
  <meta name="generator" content="webradiopi" />

  <title>"""+title+"""</title>

  <link rel="stylesheet" type="text/css" href="/styles/"""+css+""".css"/>
 </head>

 <body>
"""+body_html+"""
 </body>
</html>
"""

###
# error_page() - prints an error page
###
def error_page(errcode, errmsg, errinfo):

	body = """
  <div>
   <h1>Sorry, an error has occurred</h1>
   <p>"""+errmsg+"""</p>
   <p>Error number """+str(errcode)+"""</p>
   <p>"""+errinfo+"""</p>
  </div>
"""

	print_page("Error", body, "webradiopi")
	exit(1)

###
# is_track() - return True if the file is a music file
###
def is_track(f):
	global music_ext
	(n,e) = os.path.split(f.lower())
	return e in music_ext

###
# Do the stuff :-)
###
exit(main())