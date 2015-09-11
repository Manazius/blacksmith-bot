# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  botstatus_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

DEF_STATUS = {'message': u'пиши "хелп", чтобы понять как со мной работать', 'status': 'chat'}
STATUS_LIST = {u'ушел': 'away', u'нет': 'xa', u'занят': 'dnd', u'чат': 'chat'}

ROSTER_STATUS_FILE = 'dynamic/status.txt'

def handler_set_bot_status(type, source, body):
	if body:
		args = body.split()
		if len(args) >= 3:
			item = args[1].strip().lower()
			if item in STATUS_LIST:
				target = args[0].strip().lower()
				status = STATUS_LIST[item]
				message = body[((body.lower()).find(item) + (len(item) + 1)):].strip()
				if target in [u'везде', 'everywhere']:
					for conf in GROUPCHATS.keys():
						change_status_work(conf, message, status)
				elif target in [u'здесь', 'here']:
					if source[1] in GROUPCHATS:
						change_status_work(source[1], message, status)
					else:
						reply(type, source, u'"здесь" вовсе и не чат!')
				elif target in [u'ростер', 'roster']:
					roster_status_set(status, message)
					RST_STATUS = {'message': message, 'status': status}
					write_file(ROSTER_STATUS_FILE, str(RST_STATUS))
				elif target in GROUPCHATS:
					change_status_work(target, message, status)
				else:
					reply(type, source, u'В "%s" меня нет' % (target))
			else:
				reply(type, source, u'Статус "%s" мне неизвестен' % (item))
		else:
			reply(type, source, u'Чего-то определённо нехватает!')
	else:
		reply(type, source, u'Может чёнить самому придумать?')

def change_status_work(conf, message, status):
	STATUS[conf] = {'message': message, 'status': status}
	change_bot_status(conf, message, status)
	write_file('dynamic/%s/status.txt' % (conf), str(STATUS[conf]))

def load_conf_status(conf):
	if check_file(conf, 'status.txt', str(DEF_STATUS)):
		STATUS[conf] = eval(read_file('dynamic/%s/status.txt' % (conf)))
	else:
		delivery(u'Внимание! Не удалось создать status.txt для "%s"!' % (conf))

def roster_status_set(show_x = None, status_x = None):
	if None in [show_x, status_x]:
		if initialize_file(ROSTER_STATUS_FILE, str(DEF_STATUS)):
			RST_STATUS = eval(read_file(ROSTER_STATUS_FILE))
			Presence = xmpp.Presence(show = RST_STATUS['status'], status = RST_STATUS['message'])
		else:
			Presence = xmpp.Presence(show = DEF_STATUS['status'], status = DEF_STATUS['message'])
	else:
		Presence = xmpp.Presence(show = show_x, status = status_x)
	Presence.setTag('c', namespace = xmpp.NS_CAPS, attrs = {'node': Caps, 'ver': CapsVer})
	jClient.send(Presence)

command_handler(handler_set_bot_status, 100, "botstatus")

handler_register("01si", load_conf_status)
handler_register("02si", roster_status_set)
