# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  antiwipe.py

#  Copyleft

GoodServers =  ["jabber.ru", "xmpp.ru", # add 2ch.so maybe
				"jabber.cz", "jabbim.cz",
				"gtalk.com", "gmail.com",
				"jabbers.ru", "xmpps.ru",
				"gajim.org", "jabbim.com",
				"jabberon.ru", "jabbrik.ru",
				"talkonaut.com", "jabber.org",
				"virtualtalk.org", "xroft.ru",
				"worldskynet.net", "xmppserv.ru", "xmpp.org.ru"]

AWIPE = {}

def wipeCleaner():
	while any([desc["enabled"] for desc in AWIPE.values()]):
		time.sleep(60)
		for chat, desc in AWIPE.items():
			Chat = GROUPCHATS.get(chat)
			if not Chat:
				del AWIPE[chat]
				continue
			if desc["enabled"]:
				Time = time.time()
				for jid, Numb in desc["susps"].items():
					Numb -= 1
					if not Numb:
						del desc["susps"][jid]
				for jid, Time__ in desc["ban"].items():
					if Time - Time__ > 3599:
						none(chat, jid)
						time.sleep(0.4)
						Time += 0.4
						del desc["ban"][jid]
				for nick, desc__ in Chat.items():
					jid = handler_jid("%s/%s" % (chat, nick))
					if jid in desc["del"] and not desc__["ishere"]:
						del Chat[nick]
				desc["del"] = []
	raise SystemExit("exit")

def findServer(jid):
	dog = chr(64)
	if dog in jid:
		jid = jid.split(dog)[1]
	if chr(47) in jid:
		jid = jid.split(chr(47))[0]
	return jid

def handle_wipers(chat, nick, afl, role, status, text):
	if chat not in UNAVAILABLE:
		Time = time.time()
		jid = handler_jid("%s/%s" % (chat, nick))
		if (afl == "none") and ((time.time() - INFO['start']) > 59) and (jid not in ADLIST) and (chat in AWIPE):
			if (Time - AWIPE[chat]['ltime']) < 19:
				AWIPE[chat]["jids"].append(jid)
				joined = AWIPE[chat]["jids"]
				Numb = len(joined)
				botnick = handler_botnick(chat)
				if Numb > 2:
					AWIPE[chat]["ltime"] = Time
					server = findServer(jid)
					if (findServer(joined[Numb - 2]) == server) and (findServer(joined[Numb - 3]) == server):
						if server not in (GoodServers + [findServer(chat)]):
							outcast(chat, server, u"%s: Подозрение на вайп-атаку!" % handler_botnick(chat))
							for anyone, desc in GROUPCHATS[chat].items():
								usr_jid = handler_jid(chat + "/" + anyone)
								if findServer(usr_jid) == server and desc["ishere"]:
									kick(chat, anyone, u"%s: Подозрение на вайп-атаку!" % botnick)
									AWIPE[chat]["del"].append(jid)
						else:
							for anyone, desc in GROUPCHATS[chat].items():
								usr_jid = handler_jid(chat + "/" + anyone)
								if findServer(usr_jid) == server and desc["ishere"]:
									kick(chat, anyone, u"%s: Подозрение на вайп-атаку!" % botnick)
									if AWIPE[chat]["susps"].has_key(usr_jid):
										AWIPE[chat]["susps"][usr_jid] = 1 # Suspicious guys and number of their joinsс
									elif usr_jid in AWIPE[chat]["susps"]:
										AWIPE[chat]["susps"][usr_jid] += 1
					else:
						outcast(chat, jid, u"%s: Подозрение на вайп-атаку! (бан на час)" % handler_botnick(chat))
						AWIPE[chat]["ban"][jid] = Time
						AWIPE[chat]["del"].append(jid)
					if AWIPE[chat]["susps"].get(jid, 0) > 2:
						outcast(chat, jid, u"%s: Подозрение на вайп-атаку! (бан на час)" % handler_botnick(chat))
						AWIPE[chat]["ban"][jid] = Time
						AWIPE[chat]["del"].append(jid)
						if AWIPE[chat]["susps"].has_key(jid): 
							del AWIPE[chat]["susps"][jid]
			else:
				AWIPE[chat].update({'jids': [jid], 'ltime': Time})

def handle_wipers_(stanza, chat, old_nick, nick):
	afl = stanza.getAffiliation()
	role = stanza.getRole()
	handle_wipers(chat, nick, afl, role, "", "")

def handler_antiwipe_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/%s/antiwipe.txt' % (source[1])
			if body in [u'вкл', 'on', '1']:
				AWIPE[source[1]] = {"jids": [], "ltime": 0, "del": [], "susps": {}, "ban": {}, "enabled": True}
				write_file(filename, "True")
				reply(type, source, u'Функция антивайпа включена!')
				ThrName = wipeCleaner.func_name
				if ThrName not in ThrNames():
					composeTimer(60, wipeCleaner, ThrName).start()
			elif body in [u'выкл', 'off', '0']:
				del AWIPE[source[1]]
				write_file(filename, "False")
				reply(type, source, u'Функция антивайпа отключена!')
			else:
				reply(type, source, u'Читай помощь по команде!')
		elif source[1] in UNAVAILABLE:
			reply(type, source, u'Если бот не админ - антивайп неработоспособен...')
		elif source[1] in AWIPE:
			reply(type, source, u'Функция антивайпа включена!')
		else:
			reply(type, source, u'Функция антивайпа отключена!')
	else:
		reply(type, source, u'только в чате!')

def antiwipe_init(chat):
	if check_file(chat, 'antiwipe.txt', "True"):
		if (read_file('dynamic/%s/antiwipe.txt' % (chat)) == "True"):
			AWIPE[chat] = {"jids": [], "ltime": 0, "del": [], "susps": {}, "ban": {}, "enabled": True}
			ThrName = wipeCleaner.func_name
			if ThrName not in ThrNames():
				composeTimer(60, wipeCleaner, ThrName).start()
	else:
		delivery(u'Внимание! Не удалось создать antiwipe.txt для "%s"!' % (chat))

handler_register("04eh", handle_wipers)
handler_register("06eh", handle_wipers_)

command_handler(handler_antiwipe_control, 20, "antiwipe")

handler_register("01si", antiwipe_init)
