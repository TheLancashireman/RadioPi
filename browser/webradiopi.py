#!/usr/bin/python
import os
import urllib


music_dir = ""
music_dir_radiopi = "/home/pi/Music"
music_dir_boru = "/data/audio/jukebox"
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
	global music_dir
	global music_dir_radiopi
	global music_dir_boru

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
	# Update: lighttpd doesn't define this if there's no ?, so ignore and treat missing as blank later.
#	try:
#		query_string = os.environ["QUERY_STRING"]
#	except:
#		error_page(2005, "Server error - QUERY_STRING is not defined.", "")

	if os.path.isdir(music_dir_radiopi):
		music_dir = music_dir_radiopi
	elif os.path.isdir(music_dir_boru):
		music_dir = music_dir_boru
	else:
		error_page(2006, "Server error - music directory not found.", "")


###
# process_request() - process the query, decide what to do
###
def process_request():
	global music_dir

	try:
		query_string = urllib.unquote(os.environ["QUERY_STRING"])
	except:
		query_string = ""

#	if True:
	try:
		if query_string == "":
			front_page()
		else:
			query_list = query_string.split('&')
			if query_list[0] == "home":
				front_page()
			elif query_list[0] == "clear":
				front_page()
			elif query_list[0] == "shutdown":
				front_page()
			elif query_list[0] == "browse":
				if len(query_list) > 1:
					list_dir(query_list[1])
				else:
					list_dir("")
			else:
				error_page(1002, "Unknown command "+command+"\n", webradiopi)
#	else:
	except:
		error_page(2010, "Server error - unhandled exception processing  \""+query_string+"\".", "")

###
# front_page() - print the "home" page
###
def front_page():
	body = """
 <div>
  <h2>RadioPi menu</h2>
  <ul id="playlistcontrols">
   <li><a href="webradiopi.py?browse">Add tracks to playlist</a></li>
   <li><a href="webradiopi.py?clear">Clear playlist</a></li>
   <li><a href="webradiopi.py?shutdown">Shut down RadioPi</a></li>
  </ul>
 </div>
"""

	print_page("WebRadioPi", body, "webradiopi")

###
# list_dir() - create a page listing the contents of a specified directory relative to music_dir
###
def list_dir(rel_path):
	global music_dir
	parent = ""
	body = ""
	up_link = ""
	addall_link = ""
	directories = []
	tracks = []
	btn_open = "<img class=\"navbutton\" src=\"/images/btn-open.svg\"/>"
	btn_back = "<img class=\"navbutton\" src=\"/images/btn-back.svg\"/>"
	btn_home = "<img class=\"navbutton\" src=\"/images/btn-home.svg\"/>"
	add_cmd = "<img class=\"navbutton\" src=\"/images/btn-add.svg\" onclick=\"rp_add('"
	add_cmd_end =  "')\" alt=\"Add\" />"

	path = os.path.join(music_dir, rel_path)

	if os.path.isdir(path):
		if rel_path == "":
			dir_title = "=== Top ==="
		else:
			(parent, t2) = os.path.split(rel_path)
			if t2 == "":
				# Ended in separator
				(parent, t2) = os.path.split(parent)
			if parent == "":
				dir_title = t2
			else:
				(h,t1) = os.path.split(parent)
				dir_title = t1 + " :: " + t2

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
			addall_link = add_cmd + rel_path + add_cmd_end
		else:
			addall_link = "<img class=\"greybutton\" src=\"/images/btn-noadd.svg\"/>"

		if rel_path == "":
			up_link = "<a href=\"" + script_name + "\">" + btn_back + "</a>"
			browse_url = script_name + "?browse&"
		else:
			if parent == "":
				up_url = script_name + "?browse"
			else:
				up_url = script_name+"?browse&" + urllib.quote(parent)
			up_link = "<a href=\"" + up_url + "\">" + btn_back + "</a>"
			browse_url = script_name + "?browse&" + urllib.quote(rel_path + "/")

		body += """
  <div class="directorylisting">
   <div class="directoryentry">
    <div class="directorybutton">"""+up_link+"""</div>
    <div class="directorybutton">"""+addall_link+"""</div>
    <div class="directorytext">"""+dir_title+"""</div>
   </div>
   <div class="directoryentry"><hr/></div>
"""

		if  n_tracks > 0:
			for i in range(n_tracks):
				add_link = add_cmd + os.path.join(rel_path, tracks[i]) + add_cmd_end
				body += """
   <div class="directoryentry">
    <div class="directorybutton"><img class="greybutton" src="/images/btn-noopen.svg"/></div>
    <div class="directorybutton">"""+add_link+"""</div>
    <div class="directorytext">"""+tracks[i]+"""</div>
   </div>"""

		if  n_dirs > 0:
			for i in range(n_dirs):
				browse_link = "<a href=\"" + browse_url + urllib.quote(directories[i]) + "\">" + btn_open + "</a>"
				if has_tracks(os.path.join(path, directories[i])):
					add_link = add_cmd + os.path.join(rel_path, directories[i]) + add_cmd_end
				else:
					add_link = "<img class=\"greybutton\" src=\"/images/btn-noadd.svg\"/>"
				body += """
   <div class="directoryentry">
    <div class="directorybutton">"""+browse_link+"""</div>
    <div class="directorybutton">"""+add_link+"""</div>
    <div class="directorytext">"""+directories[i]+"""</div>
   </div>"""

		body += """
  </div>
"""
		print_page("WebRadioPi", body, "webradiopi")
	else:
		error_page(1003, "Command error: "+rel_path+" does not exist.\n", "")

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
  <script src="/script/"""+css+""".js"></script>
 </head>

 <body>
  <div class="player">
   <div class="playerbutton"><a href="/script/webradiopi.py"><img
        class="playerbutton" src="/images/btn-home.svg" alt="home"/></a></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-begin.svg" alt="begin"
        onclick="rp_cmd('begin')"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-prev.svg" alt="prev"
        onclick="rp_cmd('prev')"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-stop.svg" alt="stop"
        onclick="rp_cmd('stop')"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-toggle.svg" alt="toggle"
        onclick="rp_cmd('toggle')"/></div>
   <div class="playerbutton"><img class="playerbutton" src="/images/btn-next.svg" alt="next"
        onclick="rp_cmd('next')"/></div>
   <div class="clearall"></div>
   <hr/>
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
# has_tracks() - return True if the directory contains one or more music files
###
def has_tracks(d):
	if os.path.isdir(d):
		files = os.listdir(d)
		for f in files:
			full = os.path.join(d, f)
			if os.path.isfile(full):	# Follows symlinks
				if is_track(f):
					return True
	return False

###
# Do the stuff :-)
###
main()
exit(0)
