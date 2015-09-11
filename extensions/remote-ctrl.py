# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  remote_ctrl_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_remote_control(type, source, body):
	confs = GROUPCHATS.keys()
	confs.sort()
	if body:
		args = body.split()
		if len(args) >= 3:
			item = args[0].strip().lower()
			if item in confs:
				conf = item
			elif check_number(item):
				number = int(item) - 1
				if number >= 0 and number <= len(confs):
					conf = confs[number]
				else:
					conf = False
			else:
				conf = False
			if conf:
				mtype = args[1].strip().lower()
				if mtype == u'чат':
					msgtype = 'public'
				elif mtype == u'приват':
					msgtype = 'private'
				else:
					msgtype = False
				if msgtype:
					command = args[2].strip().lower()
					if len(args) >= 4:
						Parameters = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
					else:
						Parameters = ''
					if len(Parameters) <= 96:
						if COMMANDS.has_key(command):
							call_command_handlers(command, msgtype, [source[0], conf, source[2]], Parameters, command)
						else:
							reply(type, source, u'нет такой команды')
					else:
						reply(type, source, u'слишком длинные параметры')
				else:
					reply(type, source, u'тип указан не корректно')
			else:
				reply(type, source, u'нет такой конференции')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		col, list = 0, ''
		for conf in confs:
			col = col + 1
			list += u'\n№ '+str(col)+'. - '+conf
		reply(type, source, list)

command_handler(handler_remote_control, 100, "remote-ctrl")
