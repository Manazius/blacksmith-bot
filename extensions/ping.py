# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  ping_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

PINGSTAT = {}

def handler_ping(type, source, nick):
	user, jid = nick, nick
	if nick:
		if source[1] in GROUPCHATS:
			if nick in GROUPCHATS[source[1]]:
				if not GROUPCHATS[source[1]][nick]['ishere']:
					return reply(type, source, u'Такого пользвателя здесь нет.')
				conf_nick = source[1]+'/'+nick
				user, jid = conf_nick, handler_jid(conf_nick)
	else:
		user, jid = source[0], handler_jid(source[0])
	iq = xmpp.Iq(to = user, typ = 'get')
	INFO['outiq'] += 1
	iq.addChild('ping', {}, [], xmpp.NS_PING)
	jClient.SendAndCallForResponse(iq, handler_ping_answer, {'t0': time.time(), 'mtype': type, 'source': source, 'nick': nick, 'jid': jid, 'user': user})

def handler_ping_answer(coze, stanza, t0, mtype, source, nick, jid, user):
	if stanza:
		repl, difference = u"Понг", (time.time() - t0)
		Ping = round(difference, 3)
		if jid not in PINGSTAT:
			PINGSTAT[jid] = []
		PINGSTAT[jid].append(Ping)
		if nick:
			repl += u' от %s — %s секунд.' % (nick, str(Ping))
		else:
			repl += u' — %s секунд.' % str(Ping)
		reply(mtype, source, repl)

def form_ping_stat(jid):
	mass, col, max, min = 0, 0, 0, 999999.999
	for ping in PINGSTAT[jid]:
		mass += ping
		col += 1
		if ping < min:
			min = ping
		if ping > max:
			max = ping
	return (col, min, max, mass)

def handler_ping_stat(type, source, nick):
	if nick:
		if GROUPCHATS.has_key(source[1]) and nick in GROUPCHATS[source[1]]:
			jid = handler_jid(source[1]+'/'+nick)
		else:
			jid = nick
		if jid in PINGSTAT:
			(col, min, max, mass) = form_ping_stat(jid)
			if col:
				repl = u'\nСтатистика пинга (всего %s):\nСамый быстрый пинг — %s\nСамый медленный пинг — %s\nСреднее время пинга — %s' % (str(col), str(min), str(max), str(round(mass / col, 3)))
			else:
				repl = u'На %s статистики нет!' % (jid)
		else:
			repl = u'На %s статистики нет!' % (jid)
	else:
		jid = handler_jid(source[0])
		if jid in PINGSTAT:
			(col, min, max, mass) = form_ping_stat(jid)
			if col != 0:
				repl = u'\nСтатистика пинга (всего %s):\nСамый быстрый пинг — %s\nСамый медленный пинг — %s\nСреднее время пинга — %s' % (str(col), str(min), str(max), str(round(mass / col, 3)))
			else:
				repl = u'На тебя статистики нет!'
		else:
			repl = u'На тебя статистики нет!'
	reply(type, source, repl)

command_handler(handler_ping, 10, "ping")
command_handler(handler_ping_stat, 10, "ping")