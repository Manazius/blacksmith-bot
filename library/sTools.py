# /* encoding: utf-8 */
# Copyright sTools © simpleApps CodingTeam (Tue Oct 13 22:14:13 2011)
# This program published under GPL v3 license
# See LICENSE.GPL for more details

# OS.
import struct
import os

def getArchitecture():
	arch = 0
	if os.name == "posix":
		arch = os.uname()[4]
	elif not arch or os.name != "posix":
		from platform import processor
		arch = processor()
	if not arch:
		size = struct.calcsize("P")
		if size == 8:
			arch = "x64"
		elif size == 4:
			arch = "x32"
		else:
			arch = "Unknown Arch"
	return "[%s]" % arch

def ntDetect():
	try:
		from os import popen
		pipe = popen("ver")
		osMain = pipe.read()
		try: osMain = osMain.decode("cp866")
		except: pass
		pipe.close()
	except:
		osMain = "NT"
	del popen
	return osMain