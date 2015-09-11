# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  greetex_plugin.py

# Idea: Gigabyte [gigabyte@ngs.ru]
# Coded by: WitcherGeralt [WitcherGeralt@rocketmail.com]

greet_afls = {u'никто': 'none', u'мембер': 'member', u'админ': 'admin', u'овнер': 'owner'}

GRTX = {}

def handler_greetex(type, source, body):
	if source[1] in GROUPCHATS:
		args = body.split()
		if len(args) >= 2:
			bafl = args[0].strip().lower()
			if bafl in greet_afls:
				afl, action = greet_afls[bafl], args[1].strip().lower()
				filename = 'dynamic/%s/greetex.txt' % (source[1])
				if action in [u'добавить', 'add']:
					if len(args) >= 3:
						greet = body[((body.lower()).find(action) + (len(action) + 1)):].strip()
						if afl not in GRTX[source[1]]:
							GRTX[source[1]][afl] = []
							GRTX[source[1]][afl].append(greet)
							write_file(filename, str(GRTX[source[1]]))
							reply(type, source, u'Приветствие успешно добавлено!')
						elif greet not in GRTX[source[1]][afl]:
							GRTX[source[1]][afl].append(greet)
							write_file(filename, str(GRTX[source[1]]))
							reply(type, source, u'Приветствие успешно добавлено!')
						else:
							reply(type, source, u'Такое приветствие уже есть в базе!')
					else:
						reply(type, source, u'Само приветствие забыл добавить!')
				elif action in [u'удалить', 'del']:
					if afl in GRTX[source[1]]:
						del GRTX[source[1]][afl]
						write_file(filename, str(GRTX[source[1]]))
						reply(type, source, u'приветствия удалены!')
					else:
						reply(type, source, u'Приветствия итак не установлены!')
				elif action in [u'показать', 'show']:
					if afl in GRTX[source[1]]:
						reply(type, source, ', '.join(GRTX[source[1]][afl]))
					else:
						reply(type, source, u'Приветствия не установлены!')
				else:
					reply(type, source, u'Почитай помощь по команде!')
			else:
				reply(type, source, u'Я такого звания незнаю!')
		else:
			reply(type, source, u'Ты ничего не забыл?')
	else:
		reply(type, source, u'Так нельзя!')

def atjoin_greetex(conf, nick, afl, role, status, text):
	if (GROUPCHATS[conf][nick].get('joined', 0) - INFO['start']) >= 20:
		if afl in GRTX[conf]:
			msg(conf, random.choice(GRTX[conf][afl]).replace("%NICK%", nick))

def greetex_init(conf):
	if check_file(conf, 'greetex.txt'):
		list = eval(read_file('dynamic/%s/greetex.txt' % (conf)))
	else:
		list = {}
		delivery(u'Внимание! Не удалось создать greetex.txt для "%s"!' % (conf))
	GRTX[conf] = list

handler_register("04eh", atjoin_greetex)
command_handler(handler_greetex, 20, "greetex")

handler_register("01si", greetex_init)
