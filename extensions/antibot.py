# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  antibot_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/
#-extmanager-extVer:1.4-# 

BOTS = 'Jaskier/BlackSmith/ταλιςμαη/talisman/Talisman/Neutron/Юта/fatal/Åmulet/lesman/VIKA/iBot/Storm'.decode('utf-8')

EXCEPT_LIST = 'dynamic/exceptions.txt'

EXCEPTIONS = []
ANTIBOT_LIST = {}
ANTIBOT_MESS = []

def check_botname(item):
	for bot in BOTS.split('/'):
		if item.count(bot):
			return True
	return False

def handler_antibot_leave(conf, nick, reason, code):
	if conf not in EXCEPTIONS:
		if conf not in ANTIBOT_LIST:
			ANTIBOT_LIST[conf] = []
		jid = handler_jid(conf+'/'+nick)
		if jid in ANTIBOT_LIST[conf]:
			ANTIBOT_LIST[conf].remove(jid)

def antibot_leave(conf):
	if conf in GROUPCHATS and conf in ANTIBOT_LIST:
		if conf in EXCEPTIONS:
			del ANTIBOT_LIST[conf]
		elif len(ANTIBOT_LIST[conf]) >= 2:
			del ANTIBOT_LIST[conf]
			leave_groupchat(conf, u'Слишком много ботов!')
			delivery(u'В "%s" было слишком много ботов и я ушел!' % (conf))
		if conf in ANTIBOT_MESS:
			ANTIBOT_MESS.remove(conf)

def handler_antibot_join(conf, nick, afl, role, status, text):
	if conf in GROUPCHATS and conf not in EXCEPTIONS:
		if GROUPCHATS[conf][nick]['ishere'] and has_access(u"%s/%s" % (conf, nick), 20, nick):
			conf_nick = conf+'/'+nick
			iq = xmpp.Iq(to = conf_nick, typ = 'get')
			INFO['outiq'] += 1
			iq.addChild('query', {}, [], xmpp.NS_VERSION)
			if conf not in ANTIBOT_LIST:
				ANTIBOT_LIST[conf] = []
			jid = handler_jid(conf_nick)
			if jid not in ANTIBOT_LIST[conf]:
				jClient.SendAndCallForResponse(iq, handler_antibot_version, {'conf': conf, 'jid': jid})

def handler_antibot_version(coze, stanza, conf, jid):
	if stanza:
		if stanza.getType() == 'result':
			Props = stanza.getQueryChildren()
			for Pr in Props:
				if Pr.getName() == 'name':
					name = Pr.getData()
					if check_botname(name) and conf in ANTIBOT_LIST:
						ANTIBOT_LIST[conf].append(jid)
						if len(ANTIBOT_LIST[conf]) >= 2:
							if conf not in ANTIBOT_MESS:
								ANTIBOT_MESS.append(conf); msg(conf, u'Здесь слишком много ботов! Если в течение 15 минут лишние не будут удалены - я сваливаю...')
							try:
								composeTimer(900, antibot_leave, None, (conf,)).start()
							except:
								pass

def handler_antibot_exceptions(type, source, body):
	if body:
		args = body.split()
		if len(args) == 2:
			conf = args[1].strip().lower()
			if conf.count('@conference.') and conf.count('.') >= 2 and conf in GROUPCHATS:
				check = args[0].strip()
				if check == '+':
					if conf not in EXCEPTIONS:
						EXCEPTIONS.append(conf)
						write_file(EXCEPT_LIST, str(EXCEPTIONS))
						repl = u'добавил "%s" в список исключений.' % (conf)
					else:
						repl = u'эта конференция и так там!'
				elif check == '-':
					if conf in EXCEPTIONS:
						EXCEPTIONS.remove(conf)
						write_file(EXCEPT_LIST, str(EXCEPTIONS))
						repl = u'удалил "%s" из списка исключений.' % (conf)
					else:
						repl = u'этой конференции итак там нет'
				else:
					repl = u'инвалид синтакс'
			else:
				repl = u'что-то не то...'
		else:
			repl = u'инвалид синтакс'
	else:
		list, col = '', 0
		for conf in EXCEPTIONS:
			col = col + 1
			list += '\n'+str(col)+'. '+conf
		if col != 0:
			repl = u'\nСписок исключений "антибота":'+list
		else:
			repl = u'Список исключений пуст.'
	reply(type, source, repl)

def exceptions_cleanup():
	for x in EXCEPTIONS:
		if not GROUPCHATS.get(x):
			EXCEPTIONS.remove(x)
	write_file(EXCEPT_LIST + "_", `EXCEPTIONS`)

def antibot_exceptions_init():
	if initialize_file(EXCEPT_LIST, '[]'):
		globals()['EXCEPTIONS'] = eval(read_file(EXCEPT_LIST))
	else:
		Print('\n\nError: can`t create antibot exceptions file!', color2)
##	exceptions_cleanup()

handler_register("05eh", handler_antibot_leave)
handler_register("04eh", handler_antibot_join)
command_handler(handler_antibot_exceptions, 100, "antibot")
handler_register("00si", antibot_exceptions_init)
