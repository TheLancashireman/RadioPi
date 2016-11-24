#!/usr/bin/python
import os

music_dir = "/data/audio/jukebox"
music_ext = set([".ogg", ".mp3", ".wav", ".flac"])
script_name = ""

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
	global script_name

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

	query_string = os.environ["QUERY_STRING"]

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
		elif command == "browse":
			list_dir(query_list[1:])
		else:
			error_page(1002, "Unknown command "+command+"\n", webradiopi)

###
# front_page() - print the "home" page
###
def front_page():
	body = """
 <div>
  <h2>RadioPi menu</h2>
  <ul id="playlistcontrols">
   <li><a href="webradiopi.py?browse">Add to playlist</a></li>
   <li><a href="webradiopi.py?clear">Clear playlist</a></li>
  </ul>
 </div>
"""

	print_page("WebRadioPi", body, "webradiopi")

###
# list_dir() - create a page listing the contents of a specified directory
###
def list_dir(path_list):
	global music_dir
	body = ""
	up_link = ""
	addall_link = ""
	directories = []
	tracks = []

	if len(path_list) > 0:
		dir_title = " - ".join(path_list[len(path_list)-2:])
	else:
		dir_title = "=== Top ==="
	path = music_dir +"/"+"/".join(path_list)

	files = os.listdir(path)
	n_tracks = 0
	n_dirs = 0
	for f in sorted(files):

		full = os.path.join(path, f)

		if os.path.isdir(full):		# Follows symlinks
			directories.append(f)
			n_dirs += 1
		elif os.path.isfile(full):	# Follows symlinks
			if is_track(f):
				tracks.append(f)
				n_tracks += 1
		# Ignore all other entries
	if n_tracks > 0:
		addall_url = "#"	# fixme
		addall_link = '<a href="'+addall_url+'"><img class="navbutton" src="/images/btn-addfolder.jpg"/></a>'

	if len(path_list) > 0:
		if len(path_list) > 1:
			up_url = script_name+"?browse&"+"&".join(path_list[0:len(path_list)-1])
		else:
			up_url = script_name+"?browse"
		up_link = '<a href="'+up_url+'"><img class="navbutton" src="/images/btn-upfolder.jpg"/></a>'
		browse_url = script_name+"?browse&"+"&".join(path_list)
		add_url = script_name+"?add&"+"&".join(path_list)
	else:
		up_link = '<a href="'+script_name+'"><img class="navbutton" src="/images/btn-upfolder.jpg"/></a>'
		browse_url = script_name+"?browse"
		add_url = script_name+"?add"

	body += """
  <div>
   <table id="directorylisting">
    <tr>
     <td>"""+up_link+"""</td>
     <td>"""+addall_link+"""</td>
     <td>"""+dir_title+"""</td>
    </tr>
    <tr>
     <td></td>
     <td></td>
     <td><hr/></td>
    </tr>"""

	if  n_tracks > 0:
		for i in range(n_tracks):
			add_link = '<a href="'+add_url+'&'+tracks[i]+'">+</a>'
			body += """
    <tr>
     <td></td>
     <td>"""+add_link+"""</td>
     <td>"""+tracks[i]+"""</td>
    </tr>"""

	if  n_dirs > 0:
		for i in range(n_dirs):
			browse_link = '<a href="'+browse_url+'&'+directories[i]+'">-&gt;</a>'
			# fixme: conditional on having tracks in subdir
			add_link = '<a href="'+add_url+'&'+directories[i]+'">+</a>'
			body += """
    <tr>
     <td>"""+browse_link+"""</td>
     <td>"""+add_link+"""</td>
     <td>"""+directories[i]+"""</td>
    </tr>"""

	body += """
   </table>
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
  <div class="player">
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-home.jpg" alt="home"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-begin.jpg" alt="begin"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-prev.jpg" alt="prev"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-toggle.jpg" alt="toggle"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-stop.jpg" alt="stop"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-next.jpg" alt="next"/></div>
   <div class="clearall"/>
  </div>
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
	(n,e) = os.path.splitext(f.lower())
	return e in music_ext

###
# Do the stuff :-)
###
exit(main())
