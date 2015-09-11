# coding: utf-8
# BlackSmith plugin upgrader
# (c) simpleApps and WitcherTeam owners.
# Distributed under Apache 2.0 license on 2011 year.

import sys, os, re

if not hasattr(sys, "argv") or not sys.argv[0]:
	sys.argv = ["."]

try:
	Dir_0 = os.path.abspath(sys.argv[0])
	os.chdir(os.path.dirname(Dir_0))
except OSError:
	print "#! Incorrect launch!"
	time.sleep(6)

reload(sys)
sys.setdefaultencoding("utf-8")

## Compability handlers and vars.
CHAT_MSG_LIMIT = 0

def register_message_handler(instance):
	pass

def register_outgoing_message_handler(instance):
	pass

def register_join_handler(instance):
	pass

def register_leave_handler(instance):
	pass

def register_iq_handler(instance):
	pass

def register_presence_handler(instance):
	pass

def register_stage0_init(instance):
	pass

def register_stage1_init(instance):
	pass

def register_stage2_init(instance):
	pass

def register_stage3_init(instance):
	pass

## Main of program.
def register_command_handler(instance, command, category = [], access = 0, desc = "", syntax = "", examples = []):
	cmd = command.decode('utf-8')
	if not cmds.get(plug):
		cmds[plug] = {}
	cmds[plug][instance.func_name] = {"cmd": cmd, "desc": desc.decode("utf-8"), 
							 "syntax": syntax.decode("utf-8"),
							 "examples": [x.decode("utf-8") for x in examples]}
## "%s\nSyntax:\n\t>>> %s\nExamples:\n\t* %s" % (desc, syntax, "\n\t* ".join(examples))
	if not (desc and syntax and examples):
		print "#-# \"%\" has no \"help\""
	if not cmds_2.get(plug):
		cmds_2[plug] = {}
	cmds_2[plug][cmd] = (instance.func_name, access, plug)

def dictDot__str__(desc):
	isMultilined = lambda text: (len(text.splitlines()) > 1)
	ls = []
	for x, y in desc.items():
		if not isinstance(x, (unicode, str)):
			continue
		if not isinstance(y, (unicode, str)):
			if isinstance(y, dict):
				y = dictDot__str__(y)
			elif isinstance(y, list):
				y = "[u'''%s''']" % "''', u'''".join(y)
			else:
				y = "u'''%s'''" % unicode(y)
		else:
			y = "u'''%s'''" % y
		if isMultilined(x):
			x = repr(x)
		ls.append('u"%s": %s' % (x, y))
	return "{\n%s\n}" % (",\n\n".join(ls))


Dir = "plugins"

cmds, cmds_2 = {}, {}

for filename in sorted(os.listdir(Dir)):
	path = os.path.join(Dir, filename)
	if os.path.isdir(path) or not filename.endswith(".py"):
		print "#-# Skip: %s." % path
		continue
	plug = filename.split("_plugin")[0]
	print "#-# Plugin found: %s." % plug
	execfile(path)

Dir_2 = "help"

try:
	os.makedirs(Dir_2)
except:
	pass

for name, desc in cmds.items():
	fp = open(os.path.join(Dir_2, name), "w")
	fp.write(dictDot__str__(desc).encode("utf-8"))
	fp.close()

Dir_3 = "extensions"

try:
	os.makedirs(Dir_3)
except:
	pass

for filename in sorted(os.listdir(Dir)):
	path = os.path.join(Dir, filename)
	if os.path.isdir(path) or not filename.endswith(".py"):
		continue
	plug = filename.split("_plugin")[0]
	fp = open(path)
	ls, lines = [], fp.readlines()
	fp.close()
	for line in lines:
		line = line.strip("\r").strip("\n").rstrip()
		if line.count("# |-|-| lytic bot |-|-|"):
			line = "# BS mark.1-55"
			print "#-# Replaced header of %s." % filename
		if line.count("# -*- coding: utf-8 -*-"):
			line = "# /* coding: utf-8 */"
			print "#-# Replaced header of %s." % filename
		if line.count("Лютик Bot plugin") or line.count("Jaskier Bot plugin"):
			line = "#  BlackSmith plugin"
			print "#-# Replaced header of %s." % filename
		line = line.decode('utf-8')
		if cmds_2.get(plug):
			for cmd, desc in cmds_2[plug].items():
				if line.count(cmd) and line.count(desc[0]):
					line = 'command_handler(%s, %d, "%s")' % desc
					break
		ls.append(line)
	fp = open(os.path.join(Dir_3, plug + ".py"), "w")
	fp.write((str.join(chr(10), ls) + chr(10)).encode('utf-8'))
	print "#-# Upgraded: %s." % filename
	fp.close()
