# BS mark.1-55 plugin
# /* coding: utf-8 */

#  Initial Copyright © 2010 - 2011 WitcherGeralt [WitcherGeralt@rocketmail.com]
#  Modifications :
#		© 2011 simpleApps (http://simpleapps.ru)


TableRU = '''ёйцукенгшщзхъфывапролджэячсмитьбю.!"№;%:?*()_+/-=\ЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ.'''.decode("utf-8")
TableEN = '''`qwertyuiop[]asdfghjkl;'zxcvbnm,./!@#;%^&*()_+.-=\~QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>/'''

TurnBase = {}

def sub_desc(body, ls, sbls = None):
	if isinstance(ls, dict):
		for x, z in ls.items():
			body = body.replace(x, z)
	else:
		for x in ls:
			if isinstance(x, (list, tuple)):
				if len(x) >= 2:
					body = body.replace(x[0], x[1])
				else:
					body = body.replace(x[0], (sbls if sbls else ""))
			else:
				body = body.replace(x, (sbls if sbls else ""))
	return body

def Turn(source, body):
	desc = {}
	for nick in GROUPCHATS[source[1]].keys():
		if GROUPCHATS[source[1]][nick]["ishere"]:
			for x in (["%s%s" % (nick, Key) for Key in [":",",",">"]] + [nick]):
				if body.count(x):
					Numb = "*%s*" % str(len(desc.keys()) + 1)
					desc[Numb] = x
					body = body.replace(x, Numb)
	Turned = ""
	for x in body:
		if x in TableEN:
			Turned += TableRU[TableEN.index(x)]
		elif x in TableRU:
			Turned += TableEN[TableRU.index(x)]
		else:
			Turned += x
	return sub_desc(Turned, desc)

def command_turn(mType, source, body):
	if GROUPCHATS.get(source[1]):
		if body:
			answer = Turn(source, body)
		else:
			jid = handler_jid(source[0])
			if TurnBase[source[1]].has_key(jid):
				(Time, body) = TurnBase[source[1]].pop(jid)
				body = u"Turn\->\n[%s] <%s>: %s." % (Time, source[2], Turn(source, body))
				msg(source[1], body)
			else:
				answer = u"Ошибка."
	else:
		answer = u"Только для конференций."
	if locals().get("answer"):
		reply(mType, source, answer)

def collect_turnable(raw, mType, source, body):
	if GROUPCHATS.get(source[1]) and mType == "public" and len(source) > 2:
		jid = handler_jid(source[0])
		if jid:
			TurnBase[source[1]][jid] = (time.strftime("%H:%M:%S"), body)

def init_Turn_Base(chat):
	TurnBase[chat] = {}

def edit_Turn_Base(conf):
	del TurnBase[conf]

handler_register("01si", init_Turn_Base)
command_handler(command_turn, 10, "turn")
handler_register("01eh", collect_turnable)