# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  opros_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/
#-extmanager-extVer:0.5-#

OPROS_USERS = {}
OPROS_CHAT = []
OTOPIC = {}
MODERIN = []
STARTER = None
OPROS_GTS = {'title': False, 'ops': 0, 'tryes': 0, 'work': False}

def opros_stopped():
	globals()['STARTER'] = None
	globals()['OPROS_CHAT'] = []
	globals()['OPROS_USERS'] = {}
	globals()['OTOPIC'] = {}
	globals()['MODERIN'] = []
	globals()['OPROS_GTS'] = {'title': False, 'ops': 0, 'tryes': 0, 'work': False}

def opros_results():
	items, ovet, col = '', '', 0
	for item in OTOPIC:
		if item != 'title':
			items += u'За пункт "'+OTOPIC[item]['text']
			items += u'" проголосовало %s юзеров\n' % str(OTOPIC[item]['col'])
	for usr in OPROS_USERS:
		if OPROS_USERS[usr]['text']:
			col = col + 1
			ovet += str(col)+'. '+usr+': '+OPROS_USERS[usr]['text']+'\n'
	if col != 0:
		result = (u'\n### Мнения юзеров (высказалось %d юзеров):\n' % col)+ovet
	else:
		result = u'\n### Мнений не было высказано'
	return items+result

def opros_exe(starter):
	if OPROS_GTS['work']:
		if OPROS_GTS['tryes'] >= 36:
			msg(STARTER, (u'Опрос прошел в %s кругов, Итоги:\n\n### С опросом ознакомились %s модеров\n' % (str(OPROS_GTS['tryes']), str(len(MODERIN))))+opros_results())
			opros_stopped()
		else:
			OPROS_GTS['tryes'] += 1
			topic = OTOPIC['title']+'\n'
			items = OTOPIC.keys()
			items.sort()
			for item in items:
				if item != 'title':
					topic += item+'. '+OTOPIC[item]['text']+'\n'
			for conf in GROUPCHATS.keys():
				if conf not in OPROS_CHAT:
					OPROS_CHAT.append(conf)
					msg(conf, u'ВНИМАНИЕ!! Глобальный опрос модераторов (By %s):\n\n%s\nДля ответа напишите: "вариант" <№ варианта> или же выскажитесь словами "вариант*" <высказывание> (можно написать и то и то)' % (starter, topic))
				else:
					for user in GROUPCHATS[conf]:
						conf_user = conf+'/'+user
						if GROUPCHATS[conf][user]['ishere'] and user_level(conf_user, conf) >= 15:
							jid = handler_jid(conf_user)
							if not jid in MODERIN:
								MODERIN.append(jid)
								OPROS_USERS[jid] = {'vote': False, 'mind': False, 'text':  None}
								msg(conf_user, u'ВНИМАНИЕ!! Глобальный опрос модераторов (By %s):\n\n%s\nДля ответа напишите: "вариант" <№ варианта> или же выскажитесь словами "вариант*" <высказывание> (можно написать и то и то)' % (starter, topic))
			try:
				composeTimer(1200, opros_exe, opros_exe.func_name, (starter,)).start()
			except:
				pass

def handler_opros(type, source, body):
	if body:
		body = body.lower()
		if OPROS_GTS['ops'] <= 1 or not OPROS_GTS['title']:
			reply(type, source, u'Сначала дополни опрос (заголовок обязателен и минимум 2 пункта)')
		elif body in [u'старт', 'start']:
			if not OPROS_GTS['work']:
				OPROS_GTS['work'] = True
				globals()['STARTER'] = handler_jid(source[0])
				opros_exe(source[2])
				reply(type, source, u'Опрос стартовал')
			else:
				reply(type, source, u'Опрос уже был запущен')
		elif body in [u'стоп', 'stop']:
			if OPROS_GTS['work']:
				if type == 'public':
					reply(type, source, u'Опрос остановлен! Результат ищи в привате.')
				else:
					reply(type, source, u'Опрос остановлен!')
					time.sleep(2)
				msg(source[0], (u'Опрос прошел в %s кругов, Итоги:\n\n### С опросом ознакомились %s модеров\n' % (str(OPROS_GTS['tryes']), str(len(MODERIN))))+opros_results())
				opros_stopped()
			else:
				reply(type, source, u'А он и не был запущен')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		if OPROS_GTS['work']:
			if type == 'public':
				reply(type, source, u'смотри в приват')
			reply('private', source, (u'Прошло %s кругов опроса, Итоги на данный момент:\n\n### С опросом ознакомились %s модеров\n' % (str(OPROS_GTS['tryes']), str(len(MODERIN))))+opros_results())
		else:
			reply(type, source, u'сейчас не идёт опроса')

def handler_opros_base(type, source, body):
	if body:
		if not OPROS_GTS['work']:
			args = body.split()
			if len(args) >= 2:
				number = args[0].strip()
				text = body[(body.find(' ') + 1):].strip()
				if number.lower() in [u'заголовок', u'титл']:
					OTOPIC['title'] = text
					OPROS_GTS['title'] = True
					repl = u'Тайтл установлен'
				elif check_number(number):
					if number not in OTOPIC:
						OPROS_GTS['ops'] += 1
					OTOPIC[number] = {'col': 0, 'text': text}
					repl = u'пункт опроса добавлен'
				else:
					repl = u'помоему это не число'
			else:
				repl = u'инвалид синтакс'
		else:
			repl = u'Во время активного вопроса нельзя добавлять пункты'
	else:
		repl = u'Боди опроса:\n'
		if OTOPIC.has_key('title'):
			repl += OTOPIC['title']+'\n'
		conf = OTOPIC.keys()
		conf.sort()
		for l in conf:
			if l != 'title':
				repl += l+'. '+OTOPIC[l]['text']+'\n'
	reply(type, source, repl)

def handler_opros_otvet(type, source, body):
	if OPROS_GTS['work']:
		jid = handler_jid(source[0])
		if jid not in OPROS_USERS:
			MODERIN.append(jid)
			OPROS_USERS[jid] = {'vote': False, 'mind': False, 'text':  None}
		if OPROS_USERS[jid]['vote']:
			repl = u'Ты уже выбирал пункт'
		elif body:
			if body in OTOPIC and body != 'title':
				OPROS_USERS[jid]['vote'] = True
				OTOPIC[body]['col'] += 1
				repl = u'ваш голос учтён'
			else:
				repl = u'нет такого пункта'
		else:
			repl = u'за что голосуеш то?'
	else:
		repl = u'Сейчас нет опроса'
	reply(type, source, repl)

def handler_opros_mind(type, source, body):
	if OPROS_GTS['work']:
		jid = handler_jid(source[0])
		if jid not in OPROS_USERS:
			MODERIN.append(jid)
			OPROS_USERS[jid] = {'vote': False, 'mind': False, 'text':  None}
		if OPROS_USERS[jid]['mind']:
			repl = u'Ты уже высказал мнение'
		elif body:
			if len(body) <= 256:
				OPROS_USERS[jid] = {'vote': OPROS_USERS[jid]['vote'], 'mind': True, 'text': body}
				repl = u'ваш голос учтён'
			else:
				repl = u'слишком много текста (256 знаков предел)'
		else:
			repl = u'Ну и что же ты думаеш по этому вопросу?'
	else:
		repl = u'Сейчас нет опроса'
	reply(type, source, repl)

command_handler(handler_opros, 100, "opros")
command_handler(handler_opros_base, 100, "opros")
command_handler(handler_opros_otvet, 15, "opros")
command_handler(handler_opros_mind, 15, "opros")
