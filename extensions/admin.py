# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  admin_plugin.py

# Coded by WitcherGeralt

def handler_set_prefix(type, source, prefix):
	if source[1] in GROUPCHATS:
		if prefix:
			if prefix.lower() in [u'удалить', 'del', u'дел']:
				if source[1] in PREFIX:
					del PREFIX[source[1]]
					write_file('dynamic/%s/prefix.txt' % (source[1]), "'none'")
					reply(type, source, u'Теперь нет префикса!')
				else:
					reply(type, source, u'И так нет префикса!')
			elif prefix in cPrefs:
				PREFIX[source[1]] = prefix
				write_file('dynamic/%s/prefix.txt' % (source[1]), '"%s"' % (prefix))
				reply(type, source, u'Знак "%s" отныне является здесь префиксом.' % (prefix))
			else:
				reply(type, source, u'Недоступный префикс! Доступные: '+', '.join(cPrefs))
		elif source[1] in PREFIX:
			reply(type, source, u'Знак "%s" является префиксом здесь.' % (PREFIX[source[1]]))
		else:
			reply(type, source, u'Префикс не установлен!')
	else:
		reply(type, source, u'Не тупи! Команда только для чата!')

def handler_admin_join(type, source, body):
	if body:
		list = body.split()
		conf = list[0].strip().lower()
		if "." in conf:
			if conf not in GROUPCHATS:
				if len(list) == 2:
					code = list[1].strip()
					if code.count('{') and code.count('}'):
						codename = replace_all(code, ['{', '}'], '')
						reason = body[(body.find(code) + (len(code) + 1)):].strip() # WTF
					else:
						codename = None
						reason = body[(body.find(' ') + 1):].strip()
				else:
					codename = None
					reason = None
				jid = handler_jid(source[0])
				if jid not in [BOSS, BOSS.lower()]:
					admin_info = u'Внимание! %s (%s) загнал меня в -> "%s"' % (source[2], jid, conf)
					if reason:
						admin_info += u'\nПричина: %s' % (reason)
					delivery(admin_info)
				if codename:
					join_groupchat(conf, handler_botnick(conf), codename)
				else:
					join_groupchat(conf, handler_botnick(conf))
				time.sleep(6)
				if GROUPCHATS.has_key(conf):
					reply(type, source, u'Я зашёл в "%s"' % (conf))
					info = u'Я от %s' % (source[2])
					if reason:
						info += '\nПричина: %s' % (reason)
					msg(conf, info)
				else:
					reply(type, source, u'Не дополз до "%s"...' % (conf))
			else:
				reply(type, source, u'Я и так там! Кончай бухать!')
		else:
			reply(type, source, u'Это не конференция и я туда не пойду')
	else:
		reply(type, source, u'Ну и что же ты хочешь?')

def handler_admin_rejoin(type, source, body):
	if body:
		conf = (body.split()[0]).lower()
	else:
		conf = source[1]
	reason = u"Command «rejoin» from «%s»." % (source[2])
	if body.count(' '):
		reason += '\nReason: %s' % body[(body.find(' ') + 1):].strip()
	chats = eval(read_file(GROUPCHATS_FILE))
	if chats.has_key(conf):
		leave_groupchat(conf, reason)
		time.sleep(2)
		join_groupchat(conf, handler_botnick(conf), chats[conf]['code'])
		time.sleep(6)
		if GROUPCHATS.has_key(conf):
			reply(type, source, u'Перезашёл!')
		else:
			reply(type, source, u'Не смог перезайти в -> "%s"' % (conf))
	else:
		reply(type, source, u'Меня нет в «%s».' % (conf))

def handler_admin_leave(type, source, body):
	if body:
		list = body.split()
		conf = list[0].strip().lower()
		if len(list) == 1:
			reason = None
		else:
			reason = body[(body.find(' ') + 1):].strip()
	else:
		reason, conf = None, source[1]
	jid = handler_jid(source[0])
	if not body or jid in ADLIST or conf == source[1]:
		if conf in GROUPCHATS:
			if jid not in [BOSS, BOSS.lower()]:
				admin_info = u'Внимание! %s (%s) выгнал меня из -> "%s"' % (source[2], jid, conf)
				if reason:
					admin_info += u'\nПричина: %s' % (reason)
				delivery(admin_info)
			status = u'Меня уводит %s' % (source[2])
			if reason:
				status += u'\nПричина: %s' % (reason)
			msg(conf, status)
			time.sleep(2)
			leave_groupchat(conf, status)
			if conf != source[1]:
				reply(type, source, u'Я ушёл из -> "%s"' % (conf))
		else:
			reply(type, source, u'Меня и так там нет!')
	else:
		reply(type, source, u'Чё!? Выкуси!')

def handler_admin_restart(type, source, reason):
	status = u'Перезагрузка... Command from %s' % (source[2])
	if reason.strip() != u"тихо":
		if reason:
			status += '\nReason: %s' % (reason)
	 	for conf in GROUPCHATS.keys():
			msg(conf, status)
	time.sleep(6)
	send_unavailable(status)
	call_sfunctions("03si")
	Exit('\n\nRESTARTING...', 0, 6)

def handler_admin_exit(type, source, reason):
	status = u'Выключение... Command from %s' % (source[2])
	if reason.strip() != u"тихо":
		if reason:
			status += '\nReason: %s' % (reason)
		for conf in GROUPCHATS.keys():
			msg(conf, status)
	time.sleep(6)
	send_unavailable(status)
	call_sfunctions("03si")
	Exit('\n\n--> BOT STOPPED', 1, 12)

def handler_error_stat(type, source, body):
	if body:
		if check_number(body):
			number = int(body)
			if number in ERRORS:
				error = ERRORS[number]
				try:
					error = unicode(read_file(error))
					if type == 'public':
						reply(type, source, u'Глянь в приват.')
					msg(source[0], error)
				except:
					reply(type, source, u'Нечитаема! Попробуй посмотреть в крэшлогах.')
			else:
				reply(type, source, u'Ошибки #%s не существует!' % (body))
		else:
			reply(type, source, u'Как ни крути, «%s» не похоже ни на число, ни на номер ошибки.' % (body))
	else:
		reply(type, source, u'Всего произошло %d ошибок.' % len(ERRORS.keys()))

def handler_timeup_info(type, source, body):
	Now_time = time.time()
	start = u'\nВремя работы: %s' % (timeElapsed(Now_time - RUNTIMES['START']))
	restarts = len(RUNTIMES['REST'])
	if restarts:
		rest = (u'\nПоследняя сессия: %s\nВсего %d перезагрузок: ' % (timeElapsed(Now_time - INFO['start']), restarts))+', '.join(sorted(RUNTIMES['REST']))
	else:
		rest = u' — Работаю без перезагрузок!'
	reply(type, source, start+rest)

def handler_botup_info(type, source, body):
	if INFO['start']:
		PID, Now_time, cService = str(BOT_PID), time.time(), len(GROUPCHATS.keys())
		repl = u'\n*** Статистика работы (Bot PID: %s):\n• Рабочая сессия %s' % (PID, timeElapsed(Now_time - RUNTIMES['START']))
		if RUNTIMES['REST']:
			repl += u'\n• Последняя сессия %s' % (timeElapsed(Now_time - INFO['start']))
		repl += u'\n• Обработано %i презенсов и %i iq-запросов\n• Отправлено %i сообщений и %i iq-запросов' % (INFO['prs'], INFO['iq'], INFO['outmsg'], INFO['outiq'])
		repl += u'\n• Произошло %i ошибок и %i ошибок диспатчера\n• Получено %i сообщений\n• Выполнено %i команд' % (len(ERRORS.keys()), INFO['errs'], INFO['msg'], INFO['cmd'])
		repl += u'\n• Создано файлов: %i\n• Прочтений файлов: %i\n• Записей в файлах: %i\n• Записей крэш-логов: %i' % (INFO['fcr'], INFO['fr'], INFO['fw'], INFO['cfw'])
		if len(GROUPCHATS.keys()):
			repl += u"\n• Обслуживаю %d конференц%s" % (cService, formatWord(cService, (u"ию", u"ии", "ий")))
		memory = memory_usage()
		if memory:
			repl += u'\n• Использую %.2f МБ оперативной памяти' % (round(memory) / 1024)
		acol = 0
		for xthr in threading.enumerate():
			if xthr.isAlive():
				acol += 1
		repl += u'\n• Создано %i потоков, %i из них активно' % (INFO['thr'], acol)
		user, system = os.times()[:2]
		repl += u'\n• Потратил %.2f секунд процессора, %.2f секунд системы\n• Итог: %.2f секунд общесистемного времени' % (user, system, (user + system))
	else:
		repl = u'Кажется, я выключен...'
	reply(type, source, repl)

def handler_command_stat(type, source, body):
	if body:
		command = body.lower()
		if command in COMMSTAT:
			repl = u'Статистика по команде «%s»:\nВсего использовали: %s раз (%s юзеров)' % (command, str(COMMSTAT[command]['col']), str(len(COMMSTAT[command]['users'])))
		else:
			repl = u'Нет статистики по этой "команде"'
	else:
		list = []
		for command in COMMSTAT:
			if COMMSTAT[command]['col']:
				list.append([COMMSTAT[command]['col'], len(COMMSTAT[command]['users']), command])
		list = sorted(list, reverse = True)
		repl, col = u'\n[№][Команда][Использований][Юзеров использовало]', 0
		for item in list:
			col = col + 1
			repl += '\n%s. %s - %s (%s)' % (str(col), item[2], str(item[0]), str(item[1]))
			if col >= 20:
				break
	reply(type, source, repl)

def load_conf_prefix(conf):
	if check_file(conf, 'prefix.txt', "'none'"):
		prefix = eval(read_file('dynamic/%s/prefix.txt' % (conf)))
		if prefix != 'none':
			PREFIX[conf] = prefix
	else:
		delivery(u'Внимание! Не удалось создать prefix.txt для "%s"!' % (conf))

def crashReport_cfg(mType, source, argv):
	answer = u"Сделано."
	if argv.strip() in ["1", "вкл"]:
		if INFO["creporter"]:
			answer = u"Уже включено."
		else:
			INFO["creporter"] = 1
	elif argv.strip() in ["0", "выкл"]:
		if not INFO["creporter"]:
			answer = u"Не включено..."
		else:
			INFO["creporter"] = 0
	else:
		answer = "Вы%s подписаны на сообщения об ошибках." % ("" if INFO["creporter"] else " не")
	write_file("dynamic/creporter.txt", `INFO["creporter"]`)
	reply(mType, source, answer)

def crashReport_cfg_loader():
	if initialize_file("dynamic/creporter.txt", "1"):
		INFO["creporter"] = read_file("dynamic/creporter.txt")

command_handler(handler_set_prefix, 30, "admin")
command_handler(handler_admin_join, 80, "admin")
command_handler(handler_admin_rejoin, 80, "admin")
command_handler(handler_admin_leave, 30, "admin")
command_handler(handler_admin_restart, 100, "admin")
command_handler(handler_admin_exit, 100, "admin")
command_handler(handler_error_stat, 100, "admin")
command_handler(handler_timeup_info, 20, "admin")
command_handler(handler_botup_info, 11, "admin")
command_handler(handler_command_stat, 10, "admin")
command_handler(crashReport_cfg, 100, "admin")

handler_register("00si", crashReport_cfg_loader)
handler_register("01si", load_conf_prefix)
