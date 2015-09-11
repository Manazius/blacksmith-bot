# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  resend_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_resend(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			args = body.split()
			if len(args) >= 2:
				nick = args[0].strip()
				if nick in GROUPCHATS[source[1]] and GROUPCHATS[source[1]][nick]['ishere']:
					command = args[1].strip().lower()
					if len(args) >= 3:
						Parameters = body[((body.lower()).find(command) + (len(command) + 1)):].strip()
					else:
						Parameters = ''
					if len(Parameters) <= 96:
						if COMMANDS.has_key(command):
							jid = handler_jid(source[1]+'/'+nick)
							if jid in GLOBACCESS:
								access = GLOBACCESS[jid]
							else:
								access = False
							GLOBACCESS[jid] = 100
							if jid in ADLIST:
								admin_del = False
							else:
								ADLIST.append(jid)
								admin_del = True
							call_command_handlers(command, 'private', [source[1]+'/'+nick, source[1], nick], Parameters, command)
							time.sleep(2)
							if access:
								GLOBACCESS[jid] = access
							else:
								del GLOBACCESS[jid]
							if admin_del:
								time.sleep(4)
								ADLIST.remove(jid)
						else:
							reply(type, source, u'нет такой команды')
					else:
						reply(type, source, u'слишком длинные параметры')
				else:
					reply(type, source, u'юзеров в с таким ником здесь нет')
			else:
				reply(type, source, u'слишком мало параметров')
		else:
			reply(type, source, u'что и кому перенаправить?')
	else:
		reply(type, source, u'команда работает только в чате')

command_handler(handler_resend, 100, "resend")
