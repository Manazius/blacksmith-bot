# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  private_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_private_command(type, source, body):
	if body:
		args = body.split()
		command = args[0].strip().lower()
		if len(args) >= 2:
			Parameters = body[(body.find(' ') + 1):].strip()
		else:
			Parameters = ''
		if len(Parameters) <= 96:
			if COMMANDS.has_key(command):
				call_command_handlers(command, 'private', source, Parameters, command)
			else:
				reply(type, source, u'нет такой команды')
		else:
			reply(type, source, u'слишком длинные параметры')
	else:
		reply(type, source, u'чего хочешь то?')

command_handler(handler_private_command, 10, "private")
