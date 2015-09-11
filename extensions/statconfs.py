# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  statconfs_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

STATCONFS_FILE = 'dynamic/statconfs.txt'

STATCONFS = {'joins': 0, 'confs': {}}

def handler_statconfs(conf, nick, afl, role, status, text):
	if conf not in STATCONFS['confs']:
		STATCONFS['confs'][conf] = {}
	today = that_day()
	if today not in STATCONFS['confs'][conf]:
		STATCONFS['confs'][conf][today] = {'total': [], 'owners': [], 'admins': [], 'members': [], 'others': []}
	jid = handler_jid(conf+'/'+nick)
	if jid not in STATCONFS['confs'][conf][today]['total']:
		STATCONFS['confs'][conf][today]['total'].append(jid)
	if afl == 'owner':
		if jid not in STATCONFS['confs'][conf][today]['owners']:
			STATCONFS['confs'][conf][today]['owners'].append(jid)
	elif afl == 'admin':
		if jid not in STATCONFS['confs'][conf][today]['admins']:
			STATCONFS['confs'][conf][today]['admins'].append(jid)
	elif afl == 'member':
		if jid not in STATCONFS['confs'][conf][today]['members']:
			STATCONFS['confs'][conf][today]['members'].append(jid)
	elif jid not in STATCONFS['confs'][conf][today]['others']:
		STATCONFS['confs'][conf][today]['others'].append(jid)
	if len(STATCONFS['confs'][conf]) >= 6:
		older = 70150530
		for day in STATCONFS['confs'][conf]:
			if day < older:
				older = day
		del STATCONFS['confs'][conf][older]
	STATCONFS['joins'] += 1
	if STATCONFS['joins'] >= 24:
		STATCONFS['joins'] = 0
		write_file(STATCONFS_FILE, str(STATCONFS['confs']))

def show_statconfs(type, source, body):
	if body:
		jid = handler_jid(source[0])
		if jid in ADLIST or body == source[1]:
			if body in [u'лист', 'list']:
				today = that_day()
				list = ''
				try:
					for conf in STATCONFS['confs'].keys():
						if conf in GROUPCHATS:
							list += '\n|-| '+conf+' -->'
							confs = STATCONFS['confs'][conf].keys()
							confs.sort()
							confs.reverse()
							for day in confs:
								str_date = str(day)
								str_day = str_date[6:]+'.'+(str_date[4:])[:2]+'.'+str_date[:4]
								if day == today:
									list += u'\nСегодня (%s) ' % (str_day)
								elif (today - day) == 1:
									list += u'\nВчера (%s) ' % (str_day)
								elif (today - day) == 2:
									list += u'\nДва дня назад (%s) ' % (str_day)
								elif (today - day) == 3:
									list += u'\nТри дня назад (%s) ' % (str_day)
								elif (today - day) == 4:
									list += u'\nЧетыре дня назад (%s) ' % (str_day)
								else:
									list += u'\nНеизвестный день (%s) ' % (str_day)
								list += u'посещений - '+str(len(STATCONFS['confs'][conf][day]['total']))
								owners = len(STATCONFS['confs'][conf][day]['owners'])
								if owners != 0:
									list += u'\n\tВладельцев заходило - '+str(owners)
								admins = len(STATCONFS['confs'][conf][day]['admins'])
								if admins != 0:
									list += u'\n\tАдминов заходило - '+str(admins)
								members = len(STATCONFS['confs'][conf][day]['members'])
								if members != 0:
									list += u'\n\tУчастников заходило - '+str(members)
								others = len(STATCONFS['confs'][conf][day]['others'])
								if others != 0:
									list += u'\n\tНеместных заходило - '+str(others)
						else:
							del STATCONFS['confs'][conf]
					if list != '':
						repl = u'\nСтатистика посещений за послендние пять дней:'+list
					else:
						repl = u'Я не обслуживаю ни одной конференции!'
					if type == 'public':
						reply(type, source, u'глянь в приват')
					type = 'private'
				except RuntimeError:
					repl = u'Пока не могу, подожди пока потише не станет...'
			elif body in STATCONFS['confs']:
				today = that_day()
				repl = '\n|-| '+body+' -->'
				confs = STATCONFS['confs'][body].keys()
				confs.sort()
				confs.reverse()
				for day in confs:
					str_date = str(day)
					str_day = str_date[6:]+'.'+(str_date[4:])[:2]+'.'+str_date[:4]
					if day == today:
						repl += u'\nСегодня (%s) ' % (str_day)
					elif (today - day) == 1:
						repl += u'\nВчера (%s) ' % (str_day)
					elif (today - day) == 2:
						repl += u'\nДва дня назад (%s) ' % (str_day)
					elif (today - day) == 3:
						repl += u'\nТри дня назад (%s) ' % (str_day)
					elif (today - day) == 4:
						repl += u'\nЧетыре дня назад (%s) ' % (str_day)
					else:
						repl += u'\nНеизвестный день (%s) ' % (str_day)
					repl += u'посещений - '+str(len(STATCONFS['confs'][body][day]['total']))
					owners = len(STATCONFS['confs'][body][day]['owners'])
					if owners != 0:
						repl += u'\n\tВладельцев заходило - '+str(owners)
					admins = len(STATCONFS['confs'][body][day]['admins'])
					if admins != 0:
						repl += u'\n\tАдминов заходило - '+str(admins)
					members = len(STATCONFS['confs'][body][day]['members'])
					if members != 0:
						repl += u'\n\tУчастников заходило - '+str(members)
					others = len(STATCONFS['confs'][body][day]['others'])
					if others != 0:
						repl += u'\n\tНеместных заходило - '+str(others)
			else:
				repl = u'Хрень пишеш!'
		else:
			repl = u'У тебя доступ только к локальной статистике!'
	elif source[1] in STATCONFS['confs']:
		today = that_day()
		repl = u'\n|-| Местная статистика посещаемости -->'
		confs = STATCONFS['confs'][source[1]].keys()
		confs.sort()
		confs.reverse()
		for day in confs:
			str_date = str(day)
			str_day = str_date[6:]+'.'+(str_date[4:])[:2]+'.'+str_date[:4]
			if day == today:
				repl += u'\nСегодня (%s) ' % (str_day)
			elif (today - day) == 1:
				repl += u'\nВчера (%s) ' % (str_day)
			elif (today - day) == 2:
				repl += u'\nДва дня назад (%s) ' % (str_day)
			elif (today - day) == 3:
				repl += u'\nТри дня назад (%s) ' % (str_day)
			elif (today - day) == 4:
				repl += u'\nЧетыре дня назад (%s) ' % (str_day)
			else:
				repl += u'\nНеизвестный день (%s) ' % (str_day)
			repl += u'посещений - '+str(len(STATCONFS['confs'][source[1]][day]['total']))
			owners = len(STATCONFS['confs'][source[1]][day]['owners'])
			if owners != 0:
				repl += u'\n\tВладельцев заходило - '+str(owners)
			admins = len(STATCONFS['confs'][source[1]][day]['admins'])
			if admins != 0:
				repl += u'\n\tАдминов заходило - '+str(admins)
			members = len(STATCONFS['confs'][source[1]][day]['members'])
			if members != 0:
				repl += u'\n\tУчастников заходило - '+str(members)
			others = len(STATCONFS['confs'][source[1]][day]['others'])
			if others != 0:
				repl += u'\n\tНеместных заходило - '+str(others)
	else:
		repl = u'На данное пространство сети, чем бы оно не было, у меня статистики нет...'
	reply(type, source, repl)

def statconfs_init():
	if initialize_file(STATCONFS_FILE):
		STATCONFS['confs'] = eval(read_file(STATCONFS_FILE))
	else:
		Print('\n\nError: can`t create statconfs.txt!', color2)

def statconfs_save():
	if STATCONFS['joins']:
		write_file(STATCONFS_FILE, str(STATCONFS['confs']))

handler_register("04eh", handler_statconfs)
command_handler(show_statconfs, 20, "statconfs")
handler_register("00si", statconfs_init)
handler_register("03si", statconfs_save)
