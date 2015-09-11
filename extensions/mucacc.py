# BS mark.1-55
# /* coding: utf-8 */

#	BlackSmith plugin
#	© simpleApps, 2012 — 2013.

BanBase = {}
BanBaseFile = "dynamic/banbase.txt"

def handle_AflRl(coze, stanza, mType, source):
	if xmpp.isResultNode(stanza):
		reply(mType, source, u"Сделано.")
	else:
		reply(mType, source, u"Запрещено. Тип: %s." % stanza.getType())

def mucAccHandler(mType, source, body, func):
	chat = source[1]
	answer = ""
	if chat in GROUPCHATS:
		if body:
			args = body.split(None, 1)
			nick = args[0]
			if "." in nick or nick in GROUPCHATS[source[1]]:
				if nick in GROUPCHATS[source[1]]:
					jid = handler_jid(u"%s/%s" % (source[1], nick))
				else:
					jid = nick
				if (func.func_name in ("outcast", "kick")) and jid in ADLIST:
					answer = u"Не стоит этого делать."
				else:
					if len(args) > 1:
						reason = args[1].strip()
					else:
						reason = source[2]
					whoami = GROUPCHATS[chat].get(handler_botnick(chat), {"role": ""})["role"]
					isOwner = has_access(source[0], 30, source[1])
					if "owner" in whoami and not isOwner:
						answer = "Пока бот владелец, а ты нет, никто ничего не получит."
					else:
						if func.func_name in ("outcast", "none", "member", "admin", "owner"):
							func(source[1], jid, reason, (handle_AflRl, {"mType": mType, "source": source}))
						else:
							func(source[1], nick, reason, (handle_AflRl, {"mType": mType, "source": source}))
		else:
			answer = u"Некого."
	else:
		answer = u"Неподходящее место, не правда ли?"
	if answer: reply(mType, source, answer)

def command_kick(mType, source, body):
	mucAccHandler(mType, source, body, kick)

def command_visitor(mType, source, body):
	mucAccHandler(mType, source, body, visitor)

def command_participant(mType, source, body):
	mucAccHandler(mType, source, body, participant)

def command_moder(mType, source, body):
	mucAccHandler(mType, source, body, moderator)

def command_member(mType, source, body):
	mucAccHandler(mType, source, body, member)

def command_admin(mType, source, body):
	mucAccHandler(mType, source, body, admin)

def command_owner(mType, source, body):
	mucAccHandler(mType, source, body, owner)

def command_ban(mType, source, body):
	mucAccHandler(mType, source, body, outcast)

def command_none(mType, source, body):
	mucAccHandler(mType, source, body, none)

def command_fullban(mType, source, body):
	if body:
		args = body.split(None, 1)
		nick = args[0].strip()
		if "." in nick or nick in GROUPCHATS[source[1]]:
			if nick in GROUPCHATS[source[1]]:
				jid = handler_jid('%s/%s' % (source[1], nick))
			else:
				jid = nick
			if len(args) > 1:
				reason = args[1].strip()
			else:
				reason = source[2]
			if BanBase.get(jid):
				reply(mType, source, u"Этот пользователь уже глобально забанен.")
				return
			else:
				number = len(GROUPCHATS.keys())
				BanBase[jid] = {"date": time.strftime("%d.%m.%Y (%H:%M:%S)"),
 								"number": number,
 								"reason": reason}
				write_file(BanBaseFile, str(BanBase))
			for conf in GROUPCHATS.keys():
				outcast(conf, jid, reason)
			answer = u"«%s» успешно забанен в %d конференциях." % (jid, number)
		else:
			answer = u"Это не ник или юзеров с таким ником здесь не было."
	elif BanBase and mType == "groupchat" or source[2] in GROUPCHATS.get(source[1], []):
		answer = "\n[#] [JID] [Причина] [Кол-во чатов]\n"
		num = 0
		for jid in BanBase.keys():
			if len(BanBase[jid].values()) > 2:
				date, reason, number = BanBase[jid].values()
			else:
				date, reason = BanBase[jid].values()
				number = 0
			num += 1
			answer +=  u"\n%i. %s (%s) %s [%d]" % (num, jid, reason, date, number)
	else:
		answer = u"В базе фуллбана пусто."
	reply(mType, source, answer)

def command_fullunban(mType, source, jid):
	if jid:
		if "." in jid and not chr(32) in jid:
			if jid in BanBase:
				del BanBase[jid]
				write_file(BanBaseFile, str(BanBase))
			for conf in GROUPCHATS.keys():
				none(conf, jid)
			reply(mType, source, u'Задача выполнена в %d конференциях.' % len(GROUPCHATS.keys()))
		else:
			reply(mType, source, u'Не вижу JID.')
	else:
		reply(mType, source, u'Кого разбанивать-то?')

def banbase_init():
	if initialize_file(BanBaseFile, `{}`):
		globals()["BanBase"] = eval(read_file(BanBaseFile))
	else:
		Print('\n\nError: can`t create banbase.txt!', color2)


handler_register("00si", banbase_init)
command_handler(command_moder, 20, "mucacc")
command_handler(command_member, 20, "mucacc")
command_handler(command_admin, 30, "mucacc")
command_handler(command_owner, 30, "mucacc")
command_handler(command_kick, 15, "mucacc")
command_handler(command_visitor, 15, "mucacc")
command_handler(command_participant, 15, "mucacc")
command_handler(command_none, 20, "mucacc")
command_handler(command_ban, 20, "mucacc")
command_handler(command_fullban, 80, "mucacc")
command_handler(command_fullunban, 80, "mucacc")
