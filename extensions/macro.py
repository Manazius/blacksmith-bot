# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  macro_plugin.py

# Author:
#  dimichxp [dimichxp@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]
#  simpleApps [support@simpleapps.ru]

def handler_local_macro(type, source, Params):
	if source[1] in GROUPCHATS:
		if Params:
			keys = Params.split()
			if keys >= 2:
				cmd = keys[0].strip().lower()
				body = Params[(Params.find(' ') + 1):].strip()
				if cmd in [u'адд', '+']:
					pl = MACROS.parse_cmd(body)
					if len(pl) >= 2:
						cmd = pl[1].split()[0].lower()
						command = pl[1].split()[0].strip().lower()
						if command in COMMANDS or command in MACROS.gmacrolist or command in MACROS.macrolist[source[1]]:
							real_access = MACROS.get_access(command, source[1])
							if real_access < 0 and command in COMMAND_HANDLERS:
								real_access = COMMANDS[command]['access']
							access = True
							if real_access:
								if not has_access(source[0], real_access, source[1]):
									access = False
							if access:
								macro = pl[0].strip().lower()
								if not macro in COMMANDS:
									if not cmd in MACROS.gmacrolist and not cmd in MACROS.macrolist[source[1]]:
										MACROS.add(macro, pl[1], source[1])
										MACROS.flush(source[1], 'macr')
										reply(type, source, u'добавил')
									else:
										reply(type, source, u"Совмещение макросов противоречит системе безопасности.")
								else:
									reply(type, source, u'нельзя, так как это команда')
							else:
								reply(type, source, u'нет долступа')
						else:
							reply(type, source, u'херню пишеш')
					else:
						reply(type, source, u'инвалид синтакс')
				elif cmd in [u'дел', '-']:
					macro = body.lower()
					if macro in MACROS.macrolist[source[1]]:
						MACROS.remove(body, source[1])
						MACROS.flush(source[1])
						reply(type, source, u'убил')
					else:
						reply(type, source, u'нет такого макроса')
				elif cmd in [u'доступ', 'acc']:
					args = body.split()
					if len(args) == 2:
						macro = args[0].strip().lower()
						if not macro in COMMANDS:
							if macro in MACROS.macrolist[source[1]]:
								real_access = MACROS.get_access(macro, source[1])
								if has_access(source[0], real_access, source[1]):
									access = args[1].strip()
									if check_number(access):
										MACROS.give_access(macro, int(access), source[1])
										reply(type, source, u'вроде дал')
										time.sleep(2)
										MACROS.flush(source[1], 'sacc')
									else:
										reply(type, source, u'доступ что ты пытаешся дать не является числом')
								else:
									reply(type, source, u'нет доступа')
							else:
								reply(type, source, u'нет такого макроса')
						else:
							reply(type, source, u'нельзя, так как это команда')
					else:
						reply(type, source, u'инвалид синтакс')
				elif cmd in [u'инфо', '*']:
					if body in MACROS.macrolist[source[1]]:
						reply(type, source, body+' -> '+MACROS.macrolist[source[1]][body])
					else:
						reply(type, source, u'нет такого макроса')
				else:
					reply(type, source, u'инвалид синтакс')
			else:
				reply(type, source, u'инвалид синтакс')
		else:
			reply(type, source, u'и чего же ты хочеш?')
	else:
		reply(type, source, u'можно только в чате!')

def handler_global_macro(type, source, Params):
	if source[1] in GROUPCHATS:
		if Params:
			keys = Params.split()
			if keys >= 2:
				cmd = keys[0].strip().lower()
				body = Params[(Params.find(' ') + 1):].strip()
				if cmd in [u'адд', '+']:
					pl = MACROS.parse_cmd(body.strip())
					if len(pl) >= 2:
						macro = pl[0].strip().lower()
						cmd = pl[1].split()[0].lower()
						if not macro in COMMANDS:
							if not cmd in MACROS.gmacrolist and not cmd in MACROS.macrolist[source[1]]:
	 							MACROS.add(macro, pl[1])
								MACROS.flush(act = 'macr')
								reply(type, source, u'добавил')
							else:
								reply(type, source, u"Совмещение макросов запрещено.")
						else:
							reply(type, source, u'нельзя, так как это команда/макрос')
					else:
						reply(type, source, u'инвалид синтакс')
				elif cmd in [u'дел', '-']:
					macro = body.lower()
					if macro in MACROS.gmacrolist:
						MACROS.remove(macro)
						MACROS.flush()
						reply(type, source, u'убил')
					else:
						reply(type, source, u'нет такого макроса')
				elif cmd in [u'доступ', 'acc']:
						args = body.split()
						if len(args) == 2:
							macro = args[0].strip().lower()
							if not macro in COMMANDS:
								if macro in MACROS.gmacrolist:
									access = args[1].strip()
									if check_number(access):
										MACROS.give_access(macro, int(access))
										reply(type, source, u'вроде дал')
										time.sleep(2)
										MACROS.flush(act = 'sacc')
									else:
										reply(type, source, u'доступ, что ты пытаешься дать не является числом')
								else:
									reply(type, source, u'нет такого макроса')
							else:
								reply(type, source, u'нельзя, так как это команда')
						else:
							reply(type, source, u'что за бред?')
				elif cmd in [u'инфо', '*']:
					if body in MACROS.gmacrolist:
						macro_body = MACROS.gmacrolist[body]
						reply(type, source, body+' -> '+macro_body)
					else:
						reply(type, source, u'нет такого макроса')
				else:
					reply(type, source, u'инвалид синтакс')
			else:
				reply(type, source, u'инвалид синтакс')
		else:
			reply(type, source, u'и чего же ты хочеш?')
	else:
		reply(type, source, u'можно только в чате!')

def macrolist_handler(type, source, Params):
	if source[1] in GROUPCHATS:
		repl, dsbll, dsblg, glist, llist = u'Cписок макросов:', [], [], [], []
		if MACROS.macrolist[source[1]]:
			for macro in MACROS.macrolist[source[1]]:
				if macro in COMMOFF[source[1]]:
					dsbll.append(macro)
				else:
					llist.append(macro)
			dsbll.sort()
			llist.sort()
			repl += u'\nЛОКАЛЬНЫЕ\n'+', '.join(llist)
			if dsbll:
				repl += u'\n\nСледующие локальные макросы отключены в этой конференции:\n'+', '.join(dsbll)
		else:
			repl += u'\nнет локальных макросов'
		for macro in MACROS.gmacrolist:
			if macro in COMMOFF[source[1]]:
				dsblg.append(macro)
			else:
				glist.append(macro)
		dsblg.sort()
		glist.sort()
		if glist:
			repl += u'\nГЛОБАЛЬНЫЕ\n'+', '.join(glist)
		else:
			repl += u'\nнет глобальных макросов'
		if dsblg:
			repl += u'\n\nСледующие глобальные макросы отключены в этой конференции:\n'+', '.join(dsblg)
		if type == 'public':
			reply(type, source, u'ушёл')
		reply('private', source, repl)
	else:
		reply(type, source, u'можно только в чате!')

def macroaccess_handler(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			if body in MACROS.gaccesslist:
				repl = MACROS.gaccesslist[body]
				reply(type, source, str(repl))
			elif body in MACROS.accesslist[source[1]]:
				repl = MACROS.accesslist[source[1]][body]
				reply(type, source, str(repl))
			else:
				reply(type, source, u'нет такого макроса')
		else:
			reply(type, source, u'что за бред?')
	else:
		reply(type, source, u'можно только в чате!')

def glob_macro_files_init():
	if not check_file(file = 'macros.txt'):
		Print('\n\nError: can`t create macros.txt!', color2)
	if not check_file(file = 'macroaccess.txt'):
		Print('\n\nError: can`t create macroaccess.txt!', color2)
	try:
		MACROS.init()
	except:
		Print('\n\nError: can`t load global macro list!', color2)

def lokal_macro_files_init(conf):
	if not check_file(conf, 'macros.txt'):
		delivery(u'Внимание! Не удалось создать macros.txt для "%s"!' % (conf))
	if not check_file(conf, 'macroaccess.txt'):
		delivery(u'Внимание! Не удалось создать macroaccess.txt для "%s"!' % (conf))
	try:
		MACROS.load(conf)
	except:
		delivery(u'Внимание! Не удалось подгрузить макролист для "%s"!' % (conf))

command_handler(handler_local_macro, 20, "macro")
command_handler(handler_global_macro, 100, "macro")
command_handler(macrolist_handler, 10, "macro")
command_handler(macroaccess_handler, 10, "macro")
handler_register("00si", glob_macro_files_init)

handler_register("01si", lokal_macro_files_init)
