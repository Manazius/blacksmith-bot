# BS mark.1-55
# coding: utf-8

# regexp.py
# © simpleApps, 2013. (02.07.13 15:54)
#-extmanager-extVer:0.99.1-# 

from pattern import *

Patterns = {}

def check_jid_for_matches(jid, Patterns = None):
	if not Patterns:
		return False
	jid = JIDPattern.split(jid)
	for pattern in Patterns:
		if pattern == jid:
			return pattern
	return False


def check_nick_for_matches(nick, Patterns = None):
	if not Patterns:
		return False
	for pattern in Patterns:
		if pattern == nick:
			return pattern
	return False

def pattern_04eh(chat, nick, afl, role, status, text):
	jid = handler_jid(u"%s/%s" % (chat, nick), "full_jid")
	if nick != handler_botnick(chat):
		matched_nick = check_nick_for_matches(nick, Patterns[chat]["nick"].keys())
		if matched_nick:
			pattern_action(chat, nick, jid, matched_nick, "nick")
		else:
			matched_jid = check_jid_for_matches(jid, Patterns[chat]["jid"].keys())
			if matched_jid:
				pattern_action(chat, nick, jid, matched_jid, "jid")

def pattern_action(chat, nick, jid, matched, key):
	action = Patterns[chat][key][matched]
	Reason = "%s: Sorry, but your %s matches pattern: %s" % (handler_botnick(chat), key, matched.normalize())
	if action == "kick":
		kick(chat, nick, Reason)
	elif action == "ban":
		outcast(chat, jid, Reason)
	elif action == "visitor":
		visitor(chat, nick, Reason)
	elif action == "member":
		member(chat, jid, Reason)


def pattern_command(mType, source, body):
	room = source[1]
	if body:
		body = body.split() # 0: add/del; 1: jid/nick; 2: *@jabber.ru; 3: kick/ban/member (lol)
		if len(body) > 2:
			What = body.pop(1)
			foo = {"jid": (JIDPattern, check_jid_for_matches),	"nick": (NickPattern, check_nick_for_matches)} 
			if What in foo:
				Type = (body.pop(0)).lower()
				Pattern_raw = body.pop(0)
				if Type == "add":
					if body:
						Action = (body.pop(0)).lower()
						if Action in ("visitor", "kick", "ban", "member"):
							try:
								Pattern = foo[What][0](Pattern_raw)
							except AssertionError, text:
								answer = str(text)
							else:	
								isPatternExists = foo[What][1](Pattern_raw, Patterns[room][What].keys())
								if not isPatternExists:
									Patterns[room][What][Pattern] = Action
									write_file("dynamic/%s/%s" % (room, RegFile), str(Patterns[room]))
									answer = "Added: %(What)s match «%(Pattern_raw)s» → %(Action)s." % vars()
								else:
									answer = "Pattern «%s» already exists." % Pattern_raw
						else:
							answer = "Unknown action: %s." % action
					else:
						answer = "no body, no game"
				elif Type == "del":
					try:
						Pattern = foo[What][1](Pattern_raw, Patterns[room][What].keys())
					except AssertionError, text:
						answer = str(text)
					else:
						if Pattern:
							del Patterns[room][What][Pattern]
							write_file("dynamic/%s/%s" % (room, RegFile), str(Patterns[room]))
							answer = "ok."
						else:
							answer = "fail!"
				else:
					answer = "Undefined type!"
			else:
				answer = "Unknown parameter!"
		else:
			answer = "Need more body!"
	else:
		if Patterns.get(room):
			List = {"jid": [], "nick": []}
			nickPatterns = Patterns[room]["nick"]
			jidPatterns = Patterns[room]["jid"]
			for jPattern in sorted(jidPatterns.keys()):
				normal = jPattern.normalize()
				List["jid"].append("%s → %s" % (normal, jidPatterns[jPattern]))
			for nPattern in sorted(nickPatterns.keys()):
				normal = nPattern.normalize()
				List["nick"].append("%s → %s" % (normal, nickPatterns[nPattern]))
			answer = ""
			if List["jid"]:
				answer += "\n• JIDPatterns:\n"
				answer += enumerated_list(List["jid"])
			if List["nick"]:
				answer += "\n\n• NickPatterns:\n"
				answer += enumerated_list(List["nick"])
	if not answer:
		answer = "List is Empty." # You Are Empty dude!
	reply(mType, source, answer)

RegFile = "regexp.base"
Patterns = {}
def pattern_01si(chat):
	patterns = {"nick": {}, "jid": {}}
	if check_file(chat, RegFile, str(patterns)):
		patterns = eval(read_file("dynamic/%s/%s" % (chat, RegFile)))
	Patterns[chat] = patterns

handler_register("01si", pattern_01si)
handler_register("04eh", pattern_04eh)

command_handler(pattern_command, 20, "regexp")
