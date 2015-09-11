# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  everywhere_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_everywhere(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 2:
			mtype = args[0].strip().lower()
			if mtype == u'чат':
				msgtype = 'public'
			elif mtype == u'приват':
				msgtype = 'private'
			else:
				msgtype = False
			if msgtype:
				command = args[1].strip().lower()
				if len(args) >= 3:
					Parameters = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
				else:
					Parameters = ''
				if len(Parameters) <= 96:
					if COMMANDS.has_key(command):
						for conf in GROUPCHATS.keys():
							call_command_handlers(command, msgtype, [source[0], conf, source[2]], Parameters, command)
					else:
						reply(type, source, u'Нет такой команды.')
				else:
					reply(type, source, u'Слишком длинные параметры.')
			else:
				reply(type, source, u'Тип указан некорректно.')
		else:
			reply(type, source, u'инвалид синтакс')
	else:
		reply(type, source, u'я не умею читать мысли')

command_handler(handler_everywhere, 100, "everywhere")
