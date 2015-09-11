#! /usr/bin/python
# /* coding: utf-8 */
#  BlackSmith Bot launcher.

# (c) simpleApps CodingTeam, 2011.

import os, sys, time

interpreter = sys.executable
kernel = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'BlackSmith.py')
launch_target = interpreter + " " + kernel

del sys
while True:
	try:
		os.system(launch_target)
		time.sleep(10)
	except KeyboardInterrupt:
		raise