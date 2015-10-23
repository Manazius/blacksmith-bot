# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  vote.py

# Author:
#  Mike Mintz [mikemintz@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]
#-extmanager-extVer:1.4-#

VOTE_FILE = 'dynamic/vote.txt'

POLLINGS = {}

def handler_vote_vote(type, source, Params):
	jid = handler_jid(source[0])
	if source[1] in POLLINGS:
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'голосование было завершено')
		elif not POLLINGS[source[1]]['started']:
			reply(type, source, u'голосование ещё не запущено')
		elif type == 'public' and POLLINGS[source[1]]['options']['closed'] == True:
			reply(type, source, u'голосование закрытое, нужно голосовать у меня в привате')
		elif type == 'private' and POLLINGS[source[1]]['options']['closed'] == False:
			reply(type, source, u'голосование открытое, нужно голосовать в общем чате')
		elif not jid in POLLINGS[source[1]]['jids']:
			POLLINGS[source[1]]['jids'][jid] = {'isnotified': True, 'isvoted': False}
		elif jid in ADLIST or POLLINGS[source[1]]['jids'][jid]['isvoted'] == False:
			if POLLINGS[source[1]]['opinions'].has_key(Params):
				POLLINGS[source[1]]['opinions'][Params]['cnt'] += 1
				if POLLINGS[source[1]]['options']['nicks']:
					POLLINGS[source[1]]['opinions'][Params]['nicks'].add(source[2])
				POLLINGS[source[1]]['jids'][jid]['isvoted'] = True
				reply(type, source, u'понял')
				vote_save(source[1])
			else:
				reply(type, source, u'нет такого пункта')
		else:
			reply(type, source, u'ты уже голосовал')
	else:
		reply(type, source, u'сейчас нет никаких голосований')

def handler_vote_newpoll(type, source, Params):
	if source[1] in POLLINGS:
		if not POLLINGS[source[1]]['finished']:
			poll_text = u'ТЕКУЩЕЕ ГОЛОСОВАНИЕ\nСоздатель: '+POLLINGS[source[1]]['creator']['nick']+u'\nВопрос: '+POLLINGS[source[1]]['question']+u'\nВарианты ответов:\n'
			for opinion in sorted(POLLINGS[source[1]]['opinions']):
				poll_text += '\t'+opinion+'. '+POLLINGS[source[1]]['opinions'][opinion]['opinion']+'\n'
			poll_text += u'Чтобы проголосовать, напиши номер мнения, например "мнение 1"'
			reply(type, source, poll_text)
			return
	jid = handler_jid(source[0])
	if source[1] in POLLINGS:
		del POLLINGS[source[1]]
	if Params:
		POLLINGS[source[1]] = {'started': False, 'finished': False, 'creator': {'jid': jid, 'nick': source[2]}, 'opinions': {}, 'question': Params, 'options': {'closed': False, 'nicks': False, 'admedit': False, 'time': {'time': 0, 'start': 0}}, 'tick': None, 'jids':{}}
		reply(type, source, u'Голосование создано!\nЧтобы добавить пункты напиши "пункт+ твой_пункт". Удалить - "пункт- номер пункта".\nОпции голосования - команда "голосование*". Начать голосование - команда "голосование+". Посмотреть текущие результаты - команда "мнения". Окончить голосование - команда "итоги".\nЕсли что-то непонятно, то прочитай хелп по командам из категории "голосование"!')
		vote_save(source[1])
	else:
		reply(type, source, u'не вижу вопроса голосования')

def handler_vote_pollopinions_control(type, source, body):
	if body:
		if source[1] in POLLINGS:
			args = body.split()[0].strip()
			Params = body[(body.find(args) + len(args)):].strip()
			jid = handler_jid(source[0])
			if args == '+' or args == u'адд':
				if POLLINGS[source[1]]['started']:
					reply(type, source, u'неприменимо к запущеному голосованию, сначала останови/пересоздай')
				elif POLLINGS[source[1]]['finished']:
					reply(type, source, u'неприменимо к оконченному голосованию')
				elif jid in ADLIST or POLLINGS[source[1]]['creator']['jid'] == jid or POLLINGS[source[1]]['options']['admedit'] == True and has_access(jid, 20, source[1]):
					kcnt = len(POLLINGS[source[1]]['opinions']) + 2
					for number in range(1, kcnt):
						if str(number) not in POLLINGS[source[1]]['opinions']:
							POLLINGS[source[1]]['opinions'][str(number)] = {'opinion': Params, 'cnt': 0, 'nicks': set()}
							reply(type, source, u'добавил')
							vote_save(source[1])
				else:
					reply(type, source, u'ага, щаззз')
			elif args == '-' or args == u'дел':
				if POLLINGS[source[1]]['started']:
					reply(type, source, u'неприменимо к запущеному голосованию, сначала останови/пересоздай')
				elif POLLINGS[source[1]]['finished']:
					reply(type, source, u'неприменимо к оконченному голосованию')
				elif jid in ADLIST or POLLINGS[source[1]]['creator']['jid'] == jid or POLLINGS[source[1]]['options']['admedit'] == True and has_access(jid, 20, source[1]):
					try:
						del POLLINGS[source[1]]['opinions'][Params]
						vote_save(source[1])
						reply(type, source, u'удалил')
					except:
						reply(type, source, u'нет такого пункта')
				else:
					reply(type, source, u'ага, щаззз')
			else:
				reply(type, source, u'инвалид синтакс')
		else:
			reply(type, source, u'сейчас нет никаких голосований')
	else:
		reply(type, source, u'а дальше?')

def handler_vote_pollopinions(type, source, Params):
	if source[1] in POLLINGS:
		jid = handler_jid(source[0])
		if POLLINGS[source[1]]['finished']:
			reply(type, source, u'РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ'+vote_results(source[1]))
		elif jid in ADLIST or jid == POLLINGS[source[1]]['creator']['jid'] or POLLINGS[source[1]]['options']['admedit'] == True and has_access(jid, 20, source[1]):
			if type == 'public':
				reply(type, source, u'ушли в приват')
			reply('private', source, u'ТЕКУЩИЕ РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ'+vote_results(source[1]))
		else:
			reply(type, source, u'жди окончания голосования')
	else:
		reply(type, source, u'сейчас нет никаких голосований')

def handler_vote_polloptions(type, source, Params):
	if source[1] in POLLINGS:
		jid = handler_jid(source[0])
		if not POLLINGS[source[1]]['finished']:
			closed = POLLINGS[source[1]]['options']['closed']
			nicks = POLLINGS[source[1]]['options']['nicks']
			admedit = POLLINGS[source[1]]['options']['admedit']
			timee = POLLINGS[source[1]]['options']['time']['time']
			timest = POLLINGS[source[1]]['options']['time']['start']
			started = POLLINGS[source[1]]['started']
			if Params:
				if jid in ADLIST or POLLINGS[source[1]]['creator']['jid'] == jid or POLLINGS[source[1]]['options']['admedit'] == True and has_access(jid, 20, source[1]):
					Params = Params.split()
					if len(Params) != 2:
						reply(type, source, u'синтакс инвалид')
					elif Params[0] == 'closed':
						if Params[1] == '1':
							reply(type, source, u'приватный режим голосования включен')
							POLLINGS[source[1]]['options']['closed'] = True
						else:
							reply(type, source, u'приватный режим голосования отключен')
							POLLINGS[source[1]]['options']['closed'] = False
					elif Params[0] == 'nicks':
						if Params[1] == '1':
							reply(type, source, u'запись ников включена')
							POLLINGS[source[1]]['options']['nicks'] = True
						else:
							reply(type, source, u'запись ников отключена')
							POLLINGS[source[1]]['options']['nicks'] = False
					elif Params[0] == 'admedit':
						if Params[1] == '1':
							reply(type, source, u'теперь администрация может править голосование')
							POLLINGS[source[1]]['options']['admedit'] = True
						else:
							reply(type, source, u'теперь администрация не может править голосование')
							POLLINGS[source[1]]['options']['admedit'] = False
					elif Params[0] == 'time':
						if not Params[1] == '0':
							reply(type, source, u'время голосования %s' % timeElapsed(int(Params[1])))
							POLLINGS[source[1]]['options']['time']['time'] = int(Params[1])
							POLLINGS[source[1]]['options']['time']['start'] = time.time()
							if started:
								vote_tick(int(Params[1]), source[1])
						else:
							reply(type, source, u'время голосования - до ручного завершения')
							POLLINGS[source[1]]['options']['time']['time'] = 0
							if started:
								vote_tick(int(Params[1]), source[1], False)
					else:
						reply(type, source, u'синтакс инвалид')
					vote_save(source[1])
				else:
					reply(type, source, u'ага, щаззз')
			else:
				repl = u'ПАРАМЕТРЫ ГОЛОСОВАНИЯ:\n'
				if closed:
					repl += u'голосование проводится приватно, '
				else:
					repl += u'голосование проводится открыто, '
				if nicks:
					repl += u'ники отвечающих записываются, '
				else:
					repl += u'ники отвечающих не записываются, '
				if admedit:
					repl += u'администрация конференции имеет право редактировать голосование и просматривать его результаты, '
				else:
					repl += u'администрация конференции не имеет права редактировать голосование и просматривать его результаты, '
				if timee:
					if started:
						repl += u'голосование будет длиться %s, осталось %s' % (timeElapsed(timee), timeElapsed(timee - (time.time() - timest)))
					else:
						repl += u'голосование будет длиться %s' % timeElapsed(timee)
				else:
					repl += u'голосование будет длиться до его ручного завершения'
				reply(type, source, repl)
		else:
			reply(type, source, u'неприменимо к оконченному голосованию')
	else:
		reply(type, source, u'сейчас нет никаких голосований')

def handler_vote_endpoll(type, source, Params):
	if source[1] in POLLINGS:
		jid = handler_jid(source[0])
		if jid in ADLIST or POLLINGS[source[1]]['creator']['jid'] == jid or POLLINGS[source[1]]['options']['admedit'] == True and has_access(jid, 20, source[1]):
			POLLINGS[source[1]]['finished'] = True
			POLLINGS[source[1]]['started'] = False
			reply(type, source, u'РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ'+vote_results(source[1]))
			vote_save(source[1])
		else:
			reply(type, source, u'ага, щаззз')
	else:
		reply(type, source, u'сейчас нет никаких голосований')

def handler_vote_endpoll_tick(conf):
	POLLINGS[conf]['finished'] = True
	POLLINGS[conf]['started'] = False
	msg(conf, u'РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ'+vote_results(conf))
	vote_save(conf)


def handler_vote_join(conf, nick, afl, role, status, text):
	if conf in POLLINGS:
		jid = handler_jid(conf+'/'+nick)
		if POLLINGS[conf]['finished']:
			return
		if POLLINGS[conf]['started']:
			if not jid in POLLINGS[conf]['jids']:
				POLLINGS[conf]['jids'][jid] = {'isnotified': True, 'isvoted': False}
				poll_text = u'ТЕКУЩЕЕ ГОЛОСОВАНИЕ\nСоздатель: '+POLLINGS[conf]['creator']['nick']+u'\nВопрос: '+POLLINGS[conf]['question']+u'\nВарианты ответов:\n'
				for opinion in sorted(POLLINGS[conf]['opinions']):
					poll_text += '\t'+opinion+'. '+POLLINGS[conf]['opinions'][opinion]['opinion']+'\n'
				poll_text += u'Чтобы проголосовать, напиши номер мнения, например "мнение 1"'
				msg(conf+'/'+nick, poll_text)
				vote_save(conf)

def handler_poll_start_stop(type, source, body):
	if body:
		args = body.split()[0].strip()
		Params = body[(body.find(args) + len(args)):].strip()
		jid = handler_jid(source[0])
		if args == 'start' or args == u'стоп':
			if source[1] not in POLLINGS:
				reply(type, source, u'сейчас нет никаких голосований')
			elif POLLINGS[source[1]]['started']:
				reply(type, source, u'голосование уже запущено')
			elif POLLINGS[source[1]]['finished']:
				reply(type, source, u'голосование было завершено')
			elif len(POLLINGS[source[1]]['opinions']) == 0:
				reply(type, source, u'голосование не имеет пунктов')
			elif jid in ADLIST or POLLINGS[source[1]]['creator']['jid'] == jid or POLLINGS[source[1]]['options']['admedit'] == True and has_access(jid, 20, source[1]):
				POLLINGS[source[1]]['started'] = True
				poll_text = u'НОВОЕ ГОЛОСОВАНИЕ\nСоздатель: '+POLLINGS[source[1]]['creator']['nick']+u'\nВопрос: '+POLLINGS[source[1]]['question']+u'\nВарианты ответов:\n'
				for opinion in sorted(POLLINGS[source[1]]['opinions']):
					poll_text += '\t'+opinion+'. '+POLLINGS[source[1]]['opinions'][opinion]['opinion']+'\n'
				poll_text += u'Чтобы проголосовать, напиши номер мнения, например "мнение 1"'
				msg(source[1], poll_text)
				if POLLINGS[source[1]]['options']['time']['time']:
					if POLLINGS[source[1]]['tick']:
						if POLLINGS[source[1]]['tick'].isAlive():
							vote_tick(0, source[1])
					vote_tick(POLLINGS[source[1]]['options']['time']['time'], source[1])
					POLLINGS[source[1]]['options']['time']['start'] = time.time()
				vote_save(source[1])
			else:
				reply(type, source, u'ага, щаззз')
		elif args == 'stop' or args == u'стоп':
			if source[1] in POLLINGS:
				if POLLINGS[source[1]]['finished']:
					reply(type, source, u'неприменимо к оконченному голосованию')
				elif jid in ADLIST or POLLINGS[source[1]]['creator']['jid'] == jid or POLLINGS[source[1]]['options']['admedit'] == True and has_access(jid, 20, source[1]):
					started = POLLINGS[source[1]]['started']
					if started:
						POLLINGS[source[1]]['started'] = False
						timee = POLLINGS[source[1]]['options']['time']['time']
						timest = POLLINGS[source[1]]['options']['time']['start']
						if POLLINGS[source[1]]['options']['time']['time']:
							vote_tick(0, source[1], False)
							POLLINGS[source[1]]['options']['time']['time'] = int(timee - (time.time() - timest))
						reply(type, source, u'голосование приостановлено')
						vote_save(source[1])
					else:
						reply(type, source, u'голосование уже приостановлено')
				else:
					reply(type, source, u'ага, щаззз')
			else:
				reply(type, source, u'сейчас нет никаких голосований')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		reply(type, source, u'что тебе нужно?')

def vote_tick(timee, conf, start = True):
	if start:
		if timee:
			if POLLINGS[conf]['tick']:
				if POLLINGS[conf]['tick'].isAlive():
					POLLINGS[conf]['tick'].cancel()
			POLLINGS[conf]['tick'] = threading.Timer(timee, handler_vote_endpoll_tick,(conf,))
			try:
				POLLINGS[conf]['tick'].start()
			except:
				LAST['null'] += 1
		else:
			try:
				POLLINGS[conf]['tick'].start()
			except:
				LAST['null'] += 1
	else:
		POLLINGS[conf]['tick'].cancel()
	vote_save(conf)

def vote_save(conf):
	write_file(VOTE_FILE, str(POLLINGS))

def vote_results(conf):
	answ, cnt, allv = [], 0, 0
	poll_text = u'\nСоздатель: '+POLLINGS[conf]['creator']['nick']+u'\nВопрос: '+POLLINGS[conf]['question']+u'\nИтоги:\n'
	for opinion in POLLINGS[conf]['opinions']:
		if POLLINGS[conf]['options']['nicks']:
			answ.append([POLLINGS[conf]['opinions'][opinion]['cnt'], opinion+'. '+POLLINGS[conf]['opinions'][opinion]['opinion'], ', '.join(sorted(POLLINGS[conf]['opinions'][opinion]['nicks']))])
		else:
			answ.append([POLLINGS[conf]['opinions'][opinion]['cnt'], opinion+'. '+POLLINGS[conf]['opinions'][opinion]['opinion']])
	for opinion in sorted(answ, lambda x,y: int(x[0]) - int(y[0]), reverse = True):
		cnt += 1
		if len(opinion) == 3:
			poll_text += u'•\t'+str(cnt)+u' место и '+str(opinion[0])+u' голосов\n\tВопрос: '+opinion[1]+u'\n\tТак решили: '+opinion[2]+'\n'
			allv += opinion[0]
		else:
			poll_text += u'•\t'+str(cnt)+u' место и '+str(opinion[0])+u' голосов\n\tВопрос: '+opinion[1]+u'\n'
			allv += opinion[0]
	poll_text += u'Всего %s голосов' % str(allv)
	return poll_text

def vote_file_init():
	if initialize_file(VOTE_FILE):
		POLLINGS.update(eval(read_file(VOTE_FILE)))
	else:
		Print('\n\nError: can`t create vote.dat!', color2)

handler_register("04eh", handler_vote_join)

command_handler(handler_vote_polloptions, 20, "vote")
command_handler(handler_poll_start_stop, 20, "vote")
command_handler(handler_vote_vote, 10, "vote")
command_handler(handler_vote_pollopinions, 20, "vote")
command_handler(handler_vote_newpoll, 20, "vote")
command_handler(handler_vote_pollopinions_control, 20, "vote")
command_handler(handler_vote_endpoll, 20, "vote")

handler_register("00si", vote_file_init)
