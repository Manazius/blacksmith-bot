# BS mark.1-55
# coding: utf-8

#  BlackSmith mark.1
#  recmd.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

REINIT_FILE = 'dynamic/reinit.txt'

RECMDS = {'list': [], 'name': {}, 'access': {}}

def handler_reinit_command(type, source, body):
	if body:
		list = body.split()
		if len(list) >= 2:
			ulist = ['10', '15', '20', '30', '80', '100']
			command = list[0].strip().lower()
			rcmd = list[1].strip().lower()
			if rcmd in [u'доступ', 'acc']:
				if len(list) >= 3:
					if command in COMMANDS:
						number = list[2].strip()
						if number in ulist and check_number(number):
							access = int(number)
							if access != COMMANDS[command]['access']:
								RECMDS['access'][command] = COMMANDS[command]['access']
								COMMANDS[command]['access'] = access
								reinit_record_handler(command, access)
								reply(type, source, u'Доступ "%s" = %s' % (command, number))
							else:
								reply(type, source, u'Гг так ведь и есть...')
						else:
							reply(type, source, u'Неа! В топку! Нормальные доступы: '+', '.join(ulist))
					else:
						reply(type, source, u'нет такой команды')
				else:
					reply(type, source, u'мало аргументов!')
			elif rcmd in [u'имя', 'name']:
				if len(list) >= 3:
					if command in COMMANDS:
						new_cmd = list[2].strip().lower()
						if command != new_cmd:
							if new_cmd not in COMMANDS and new_cmd not in RECMDS['name']:
								if command not in RECMDS['list']:
									if len(new_cmd) <= 12:
										RECMDS['name'][command] = {'cmd': new_cmd, 'list': COMMANDS[command]}
										if len(list) >= 4:
											x = list[3].strip()
											if x.count('!'):
												x = x.replace('!', '')
												if x in ulist and check_number(x):
													COMMANDS[command]['access'] = int(x)
										COMMANDS[new_cmd] = COMMANDS[command]
										del COMMANDS[command]
										COMMAND_HANDLERS[new_cmd] = COMMAND_HANDLERS[command]
										COMMSTAT[new_cmd] = {'col': 0, 'users': []}
										cmd_mass = {'command': command, 'list': COMMANDS[new_cmd]}
										RECMDS["list"].append(new_cmd)
										reinit_record_handler(new_cmd, cmd_mass)
										reply(type, source, u'Теперь вместо "%s" будет "%s"' % (command, new_cmd))
									else:
										reply(type, source, u'нельзя более 12ти символов!')
								else:
									reply(type, source, u'она и так была переименована!')
							else:
								reply(type, source, u'мне это кажется, или ты хернёй сейчас страдаешь?')
						else:
							reply(type, source, u'по-моему ты меня троллишь :lol:')
					else:
						reply(type, source, u'нет такой команды')
				else:
					reply(type, source, u'мало аргументов!')
			elif rcmd in [u'внорму', 'backup']:
				if command in RECMDS['access']:
					COMMANDS[command]['access'] = RECMDS['access'][command]
					del RECMDS['access'][command]
					reinit_record_handler(command)
					reply(type, source, u'Доступ "%s" = %d' % (command, COMMANDS[command]['access']))
				elif command in RECMDS['name']:
					del_cmd = RECMDS['name'][command]['cmd']
					RECMDS['list'].remove(del_cmd)
					del COMMANDS[del_cmd]
					COMMANDS[command] = RECMDS['name'][command]['list']
					del RECMDS['name'][command]
					reinit_record_handler(del_cmd)
					del COMMAND_HANDLERS[del_cmd]
					reply(type, source, u'команда "%s" - теперь в норме!' % (command))
				else:
					reply(type, source, u'команда "%s" - и так в норме!' % (command))
			else:
				reply(type, source, u'чего нужно?')
		else:
			reply(type, source, u'мало аргументов!')
	else:
		repl = u'\nКоманды с изменённым именем:\n'
		rn_cmds = RECMDS['name'].keys()
		rn_col = 0
		if len(rn_cmds) != 0:
			for cmd in rn_cmds:
				rn_col = rn_col + 1
				repl += '%d. %s --> %s\n' % (rn_col, cmd, RECMDS['name'][cmd]['cmd'])
		else:
			repl += u'\tотсутствуют'
		repl += u'\nКоманды с изменённым доступом:\n'
		ra_cmds = RECMDS['access'].keys()
		ra_col = 0
		if len(ra_cmds) != 0:
			for cmd in ra_cmds:
				ra_col += 1
				repl += u'%d. %s\nDefault доступ = %d\nТекущий доступ = %d\n' % (ra_col, cmd, RECMDS['access'][cmd], COMMANDS[cmd]['access'])
		else:
			repl += u'\tотсутствуют'
		reply(type, source, repl)

def reinit_record_handler(cmd, cmd_mass = None):
	REINIT_LIST = eval(read_file(REINIT_FILE))
	if cmd_mass:
		REINIT_LIST[cmd] = cmd_mass
	else:
		del REINIT_LIST[cmd]
	write_file(REINIT_FILE, str(REINIT_LIST))

def reinit_commands():
	if initialize_file(REINIT_FILE):
		REINIT_LIST = eval(read_file(REINIT_FILE))
		for command in REINIT_LIST:
			if command in COMMANDS:
				RECMDS['access'][command] = COMMANDS[command]['access']
				COMMANDS[command]['access'] = REINIT_LIST[command]
			else:
				try:
					true_cmd = REINIT_LIST[command]['command']
					if true_cmd in COMMANDS:
						COMMANDS[command] = REINIT_LIST[command]['list']
						RECMDS['name'][true_cmd] = {'cmd': command, 'list': COMMANDS[true_cmd]}
						RECMDS['list'].append(command)
						del COMMANDS[true_cmd]
						COMMAND_HANDLERS[command] = COMMAND_HANDLERS[true_cmd]
						COMMSTAT[command] = {'col': 0, 'users': []}
				except:
					Print('\n\nError: can`t reinit one of the commands!', color2)
	else:
		Print('\n\nError: can`t create commands reinit file!', color2)

command_handler(handler_reinit_command, 100, "recmd")

handler_register("00si", reinit_commands)
