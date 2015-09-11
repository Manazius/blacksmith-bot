# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  info_plugin.py

# Author:
#  Als [Als@exploru.net]
# Modifications:
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

def handler_true_jid(type, source, nick):
	if nick:
		if source[1] in GROUPCHATS:
			if nick in GROUPCHATS[source[1]]:
				jid = handler_jid(source[1]+'/'+nick)
				if type == 'public':
					reply(type, source, u'ушёл')
				reply('private', source, u'Реальный JabberID «%s» — %s.' % (nick, jid))
			else:
				reply(type, source, u'Ты уверен, «%s» что был тут?' % (nick))
		else:
			reply(type, source, u'Только для чатов')
	else:
		reply(type, source, u'Команда требует наличия параметров.')

def handler_online_here(type, source, body):
	if source[1] in GROUPCHATS:
		stalker = handler_jid(source[0])
		list = ''
		col = 0
		for usr in GROUPCHATS[source[1]]:
			if GROUPCHATS[source[1]][usr]['ishere']:
				col = col + 1
				list += '\n'+str(col)+'. '+usr
				if stalker in ADLIST:
					list += ' ('+handler_jid(source[1]+'/'+usr)+')'
		if type == 'public':
			reply(type, source, u'Отправил в приват, на всякий...')
		reply('private', source, (u'Я здесь вижу %s юзеров:' % str(col))+list)
	else:
		reply(type, source, u'Только для чатов.')

command_handler(handler_true_jid, 20, "info")
command_handler(handler_online_here, 10, "info")
