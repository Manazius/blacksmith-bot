# BS mark.1-55
# coding: utf-8

#  BlackSmith mark.1
#  more.py

#  Code © (2012) by WitcherGeralt [alkorgun@gmail.com]

def command_more(ltype, source, body):
	if ltype == "public":
		if MORE.get(source[1]):
			body = "[&&] %s" % (MORE[source[1]])
			MORE[source[1]] = ""
			msg(source[1], body)

command_handler(command_more, 10, "more")
