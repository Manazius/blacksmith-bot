# BS mark.1-55
# coding: utf-8

#  BlackSmith plugin
#  help.py

#  © simpleApps & WitcherGeralt, 2011 — 2013.

def command_comaccess(type, source, body):
	if body:
		command = body.lower()
		if command in COMMANDS:
			access = COMMANDS[command]['access']
			reply(type, source, u"Доступ к команде «%s» — %s." % (command, str(access)))
		else:
			reply(type, source, u"Нет такой команды.")
	else:
		reply(type, source, u'И что?')

def command_help(type, source, body):
	if body:
		command = body.lower()
		if len(command) <= 24:
			if command in COMMANDS:
				try:
					if COMMANDS[command].has_key('desc'):
						fr = COMMANDS[command]
					else:
						plug = COMMANDS[command]['plug']
						inst = COMMAND_HANDLERS[command].func_name
						fr = eval(read_file("help/%s" % plug).decode("utf-8"))[inst]
					mess = fr['desc']
					mess += u'\nИспользование:\n»»» '+fr['syntax']+u'\nПримеры:'
					for example in fr['examples']:
						mess += '\n    »»» '+example
					mess += u'\nМинимальный уровень доступа: '+str(COMMANDS[command]['access'])
				except:
					mess = u'Нет помощи для данной команды.'
			else:
				mess = u'Нет такой команды, чтобы узнать точный список напиши "комлист"'
		else:
			mess = u'Команды длиннее 24-х символов не существует!'
	else:
		mess = u'Для просмотра списка команд, напишите «комлист».'
	reply(type, source, mess)

def command_comlist(mType, source, body):
	answer = ""
	commandByAccess = {}
	Access = {0: "Никто", 
			  10: "Участник", 
			  11: "Зарегистрированный пользователь", 
			  15: "Модератор", 
			  20: "Администратор", 
			  30: "Владелец", 
			  80: "Шеф", 
			  100: "Владелец бота"}
	for command in COMMANDS.keys():
		access = COMMANDS[command]["access"]
		if access not in commandByAccess.keys():
			commandByAccess[access] = []
		commandByAccess[access].append(command)
	for access in sorted(commandByAccess.keys()):
		answer += "\n## Команды для пользователей с доступом %d (%s):\n" % (access, Access.get(access, "Unknown"))
		answer += str.join(", ", sorted(commandByAccess[access])) + "\n"
	if mType == "public":
		reply(mType, source, "В привате.")
	msg(source[0], answer)

def command_commands(mType, source, body):
	commands = COMMANDS.keys()
	answer = u"\nСписок команд в категории \"все\" (всего %d штук):\n\n%s." % (len(commands), ", ".join(sorted(commands)))
	if len(COMMOFF.get(source[1], [])):
		answer += u"\n\nСледующие команды здесь отключены: \n%s." % ", ".join(sorted(COMMOFF.get(source[1], [])))
	answer += u"\n\n*** Чтобы узнать доступ к определённой команде, напишите \"комдоступ [команда]\"."
	if PREFIX.get(source[1]):
		answer += u"\n*** Префикс команд: \"%s\"." % PREFIX.get(source[1])
	if mType != "private":
		reply(mType, source, u"В привате.")	
	msg(source[0], answer)


command_handler(command_comaccess, 10, "help")
command_handler(command_help, 10, "help")
command_handler(command_comlist, 10, "help")
command_handler(command_commands, 10, "help")
