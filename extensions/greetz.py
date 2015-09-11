# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  greetz_plugin.py

#  Idea: Als [Als@exploit.in]
#  Coded by: WitcherGeralt [WitcherGeralt@rocketmail.com]

GREETZ = {}

def handler_greet(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split('=', 1)
			if len(args) == 2:
				item = args[0].strip()
				if item in GROUPCHATS[source[1]]:
					jid = handler_jid(source[1]+'/'+item)
				elif item.count('@') and item.count('.') and not item.count(' '):
					jid = item
				else:
					jid = False
				if jid:
					filename = 'dynamic/'+source[1]+'/greetz.txt'
					greet = args[1].strip()
					if greet.lower() in [u'нет', 'none', '*', 'show']:
						if jid in GREETZ[source[1]]:
							if greet.lower() in [u'нет', 'none']:
								del GREETZ[source[1]][jid]
								write_file(filename, str(GREETZ[source[1]]))
								reply(type, source, u'Приветствие удалено!')
							else:
								reply(type, source, GREETZ[source[1]][jid])
						else:
							reply(type, source, u'На него нет приветствия!')
					else:
						GREETZ[source[1]][jid] = greet
						write_file(filename, str(GREETZ[source[1]]))
						reply(type, source, u'Приветствие установлено!')
				else:
					reply(type, source, u'Незнаю я такого юзера...')
			else:
				reply(type, source, u'Читай помощь по команде!')
		else:
			reply(type, source, u'Инвалид синтакс!')
	else:
		reply(type, source, u'Отвали!')

def atjoin_greetz(chat, nick, afl, role, status, text):
	if (GROUPCHATS[chat][nick]['joined'] - INFO['start']) >= 20:
		jid = handler_jid(chat+'/'+nick)
		if jid in GREETZ.get(chat):
			msg(chat, '%s: %s' % (nick, GREETZ[chat][jid]))

def greetz_init(chat):
	if check_file(chat, 'greetz.txt'):
		list = eval(read_file('dynamic/'+chat+'/greetz.txt'))
	else:
		list = {}
		delivery(u'Внимание! Не удалось создать greetz.txt для "%s"!' % (chat))
	GREETZ[chat] = list

command_handler(handler_greet, 20, "greetz")
handler_register("04eh", atjoin_greetz)

handler_register("01si", greetz_init)
