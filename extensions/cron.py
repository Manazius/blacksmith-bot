# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  cron_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

CRCMDS = [u'пинг', u'тест', u'сказать', u'чисть', u'анекдот', u'ботап', u'фоменко', u'рейтинг', 'днс', 'порт']

CRON = {'col': 0, 'tmrs': {}}

def len_cron():
	col = 0
	for timer in CRON['tmrs']:
		if CRON['tmrs'][timer].isAlive():
			col += 1
	return col

def cron_bust_handler(timer, cycles):
	over_time = timer*cycles
	if over_time > 86400:
		return u'Общее время cron`a не должно составлять больше 24х часов!'
	elif cycles < 2:
		return u'Меньше 2х циклов бессмысленно! Юзай таймер!'
	elif timer < 60:
		return u'Меньше минуты бессмысленно!'
	return False

def execute_cron_handler(commnad_handler, timer, cycles, command, type, source, body):	
	cycles -= 1
	if cycles:
		try:
			commnad_handler(type, source, body)
		except:
			lytic_crashlog(commnad_handler, command)
		NUM = len(CRON['tmrs']) + 1
		CRON['tmrs'][NUM] = composeTimer(timer, execute_cron_handler, None, (commnad_handler, timer, cycles, command, type, source, body))
		try:
			CRON['tmrs'][NUM].start()
		except:
			try:
				del CRON['tmrs'][NUM]
			except:
				pass


def handler_cron_command(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			timer = args[0].strip()
			if check_number(timer):
				jid = handler_jid(source[0])
				timer = int(timer)
				cycles = args[1].strip()
				if cycles.lower() in [u'стоп', 'stop']:
					if jid in ADLIST:
						if timer in CRON['tmrs']:
							if CRON['tmrs'][timer].isAlive():
								try:
									CRON['tmrs'][timer].cancel()
								except:
									reply(type, source, u'Ошибка! Не удалось остановить cron!')
								else:
									reply(type, source, u'Cron остановлен!')
							else:
								reply(type, source, u'Cron итак уже остановлен!')
						else:
							reply(type, source, u'Нет такого таймера[цикла]!')
					else:
						reply(type, source, u'Эй! Ты не суперадмин!')
				elif len_cron() <= 15:
					if len(args) >= 3:
						if check_number(cycles):
							cycles = int(cycles) + 1
							bust = cron_bust_handler(timer, cycles)
							if bust:
								reply(type, source, bust)
							else:
								command = args[2].strip().lower()
								if command in CRCMDS or jid in ADLIST: # BOSS?
									if len(args) >= 4:
										Params = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
										print Params
										print body
									else:
										Params = ''
									if len(Params) <= 96:
										if COMMANDS.has_key(command):
											if COMMAND_HANDLERS.has_key(command):
												NUM = len(CRON['tmrs']) + 1
												handler = COMMAND_HANDLERS[command]
												CRON['tmrs'][NUM] = composeTimer(timer, execute_cron_handler, None, (handler, timer, cycles, command, type, source, Params))
												try:
													CRON['tmrs'][NUM].start()
												except:
													try:
														del CRON['tmrs'][NUM]
													except:
														pass
													reply(type, source, u'Ошибка! Не удалось создать cron!')
												else:
													CRON['col'] += 1
													reply(type, source, u'Через каждые %s буду выполнять твою команду' % timeElapsed(timer))
										else:
											reply(type, source, u'нет такой команды')
									else:
										reply(type, source, u'слишком длинные параметры')
								else:
									reply(type, source, u'Cron на эту команду для тебя недоступен\nДоступны следующие таймеры: '+', '.join(sorted(CRCMDS)))
						else:
							reply(type, source, u'Ты указал неверное колличество циклов!')
					else:
						reply(type, source, u'Инвалид синтакс!')
				else:
					reply(type, source, u'Сейчас активно 16 таймеров[циклов], больше нельзя!')
			else:
				reply(type, source, u'Ты указал неверное время цикла!')
		else:
			reply(type, source, u'Инвалид синтакс!')
	else:
		alive = ''
		for timer in CRON['tmrs']:
			if CRON['tmrs'][timer].isAlive():
				alive += str(timer)+' *'
		if alive:
			list = u' таймеров[циклов]\n- %s из них активно активно (PIDs): %s' % (str(len_cron()), alive)
		else:
			list = u' таймеров[циклов] - все завершены'
		if CRON['col'] != 0:
			repl = u'\nВсего было активировано '+str(CRON['col'])+list
		else:
			repl = u'Пока небыло запущено ни одного сron`а'
		reply(type, source, repl)

command_handler(handler_cron_command, 20, "cron")
