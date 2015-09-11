# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  macrokill_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_set_botnick(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			nick = replace_all(body, {' ': '_', '"': '', "'": ''})
			if len(nick) <= 16:
				BOT_NICKS[source[1]] = nick
				save_conflist(source[1], nick)
				send_join_presece(source[1], nick)
				reply(type, source, u'Переименовался в "%s"' % (nick))
			else:
				reply(type, source, u'Нее! в моём нике не более 16 символов!')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		reply(type, source, u'Только для чатов.')

def handler_conflist(type, source, body):
	repl = u'\n№ [Конфа] [Ник] [Pfx] [Юзеров] [статус]'
	col = 0
	for conf in sorted(GROUPCHATS.keys()):
		col = col + 1
		online = 0
		botnick = handler_botnick(conf)
		for user in GROUPCHATS[conf]:
			if GROUPCHATS[conf][user]['ishere']:
				online = online + 1
		if conf in PREFIX:
			pfx = PREFIX[conf]
		else:
			pfx = u'нет'
		if conf in UNAVAILABLE:
			ismoder = u'Внимание!! Нет прав!!'
		else:
			ismoder = u'модер'
		repl += '\n%s. %s [%s] "%s" (%s) - %s' % (str(col), conf.split('@')[0], botnick, pfx, str(online), ismoder)
	if col != 0:
		if type == 'public':
			reply(type, source, u'глянь в приват')
		reply('private', source, repl)
	else:
		reply(type, source, u'А меня нет ни в одной конверенции!')

def command_chatlist(mType, source, args):
	if not args:
		cList = u"\nСписок конференций, в которых"\
			u" сидит бот (всего %d штук):\n" % len(GROUPCHATS.keys())
		for x, y in enumerate(sorted(GROUPCHATS.keys())):
			cList += u"%d. %s\n" % (x + 1, y)
		if mType == "public":
			reply(mType, source, u"Смотри в привате.") 
		reply("private", source, cList)
	elif args.strip() == "количество":
		reply(mType, source, u"Количество обслуживаемых конференций: %d." % len(GROUPCHATS.keys()))
	else:
		a0, a1 = a
	

def handler_visitors(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			action = body.lower()
		else:
			action = 'default'
		if action in [u'сегодня', 'today']:
			today = that_day()
			userlist = ''
			usrcol = 0
			col = 0
			for user in sorted(GROUPCHATS[source[1]].keys()):
				if not GROUPCHATS[source[1]][user]['ishere']:
					join_date = GROUPCHATS[source[1]][user]['join_date']
					if today == join_date[0]:
						usrcol = usrcol + 1
						userlist += '\n%s. %s (%s)' % (str(usrcol), user, handler_jid(source[1]+'/'+user))
				else:
					col = col + 1
			if usrcol != 0:
				if type == 'public':
					reply(type, source, u'глянь в приват')
				reply('private', source, (u'Сегодня здесь было %s юзеров:' % str(usrcol))+userlist+(u'\n+ ещё %s досихпор здесь' % str(col)))
			else:
				reply(type, source, u'Сегодня при мне ещё никто не выходил, все кто был досихпор здесь!')
		elif action in [u'даты', 'dates']:
			userlist = ''
			usrcol = 0
			for user in sorted(GROUPCHATS[source[1]].keys()):
				usrcol = usrcol + 1
				join_date = GROUPCHATS[source[1]][user]['join_date']
				userlist += '\n%s. %s %s' % (str(usrcol), user, time.strftime('%d.%m.%Y (%H:%M:%S)', join_date[1]))
			if type == 'public':
				reply(type, source, u'глянь в приват')
			reply('private', source, (u'При мне заходило %s юзеров:' % str(usrcol))+userlist)
		elif action in [u'лист', 'list']:
			users = []
			for user in GROUPCHATS[source[1]]:
				users.append(user)
			usrcol = len(users)
			if type == 'public':
				reply(type, source, u'глянь в приват')
			reply('private', source, (u'При мне заходило %s юзеров: ' % str(usrcol))+', '.join(sorted(users)))
		else:
			userlist = ''
			usrcol = 0
			col = 0
			for user in sorted(GROUPCHATS[source[1]].keys()):
				if not GROUPCHATS[source[1]][user]['ishere']:
					usrcol = usrcol + 1
					userlist += '\n%s. %s (%s)' % (str(usrcol), user, handler_jid(source[1]+'/'+user))
				else:
					col = col + 1
			if usrcol != 0:
				if type == 'public':
					reply(type, source, u'глянь в приват')
				reply('private', source, (u'Здесь было %s юзеров:' % str(usrcol))+userlist+(u'\n+ ещё %s до сих пор здесь' % str(col)))
			else:
				reply(type, source, u'При мне никто ещё не выходил, все, кто был, - до сих пор здесь!')
	else:
		reply(type, source, u'Я хз кто был у тебя в ростере :D')

def handler_topic(type, source, body):
	if body:
		body = replace_all(body, {'<': u'«', '>': u'»'})
		try:
			jClient.send(xmpp.Message(unicode(source[1]), "", "groupchat", body))
		except:
			reply(type, source, u'Не отправляется как-то эта хрень...')
	else:
		reply(type, source, u'И где тут топег?')

command_handler(handler_set_botnick, 30, "macrokill")
command_handler(handler_visitors, 20, "macrokill")
command_handler(handler_conflist, 20, "macrokill")
command_handler(command_chatlist, 20, "macrokill")
command_handler(handler_topic, 20, "macrokill")
