# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  most_plugin.py

# Coded by: 40tman (40tman@qip.ru)
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)

MOST_C1 = None
MOST_C2 = None

def most_message_handler(raw, type, source, body):
	if type == 'public' and source[1] in [MOST_C1, MOST_C2]:
		if source[1] == MOST_C1:
			msg(MOST_C2, 'from: <'+source[2]+'>,\n'+body)
		elif source[1] == MOST_C2:
			msg(MOST_C1, 'from: <'+source[2]+'>,\n'+body)

def most_join_handler(chat, nick, afl, role, status, text):
	if chat in [MOST_C1, MOST_C2]:
		conf = chat.split('@')[0]
		if chat == MOST_C1:
			msg(MOST_C2, u'(%s@..): %s подключился как %s & %s' % (conf, nick, afl, role))
		elif chat == MOST_C2:
			msg(MOST_C1, u'(%s@..): %s подключился как %s & %s' % (conf, nick, afl, role))

def most_leave_handler(chat, nick, reason, code):
	if chat in [MOST_C1, MOST_C2]:
		conf = chat.split('@')[0]
		if code:
			if code == '307':
				if reason:
					if chat == MOST_C1:
						msg(MOST_C2, '(%s@..): %s has been kicked (%s)' % (conf, nick, reason))
					elif chat == MOST_C2:
						msg(MOST_C1, '(%s@..): %s has been kicked (%s)' % (conf, nick, reason))
				else:
					if chat == MOST_C1:
						msg(MOST_C2, '(%s@..): %s has been kicked' % (conf, nick))
					elif chat == MOST_C2:
						msg(MOST_C1, '(%s@..): %s has been kicked' % (conf, nick))
			elif code == '301':
				if reason:
					if chat == MOST_C1:
						msg(MOST_C2, '(%s@..): %s has been banned (%s)' % (conf, nick, reason))
					elif chat == MOST_C2:
						msg(MOST_C1, '(%s@..): %s has been banned (%s)' % (conf, nick, reason))
				else:
					if chat == MOST_C1:
						msg(MOST_C2, '(%s@..): %s has been banned (%s)' % (conf, nick))
					elif chat == MOST_C2:
						msg(MOST_C1, '(%s@..): %s has been banned (%s)' % (conf, nick))
		elif reason:
			if chat == MOST_C1:
				msg(MOST_C2, '(%s@..): %s leaves the room (%s)' % (conf, nick, reason))
			elif chat == MOST_C2:
				msg(MOST_C1, '(%s@..): %s leaves the room (%s)' % (conf, nick, reason))
		else:
			if chat == MOST_C1:
				msg(MOST_C2, '(%s@..): %s leaves the room' % (conf, nick))
			elif chat == MOST_C2:
				msg(MOST_C1, '(%s@..): %s leaves the room' % (conf, nick))

def handler_most_create(type, source, body):
	if type != 'private' or handler_jid(source[0]) in ADLIST:
		if body:
			if body in GROUPCHATS:
				if MOST_C1 == None and MOST_C2 == None:
					globals()['MOST_C1'] = source[1]
					globals()['MOST_C2'] = body
					msg(MOST_C1, u'Мост между "%s" & "%s" открыт! (закрыть мост можно по команде "мост_дел")' % (MOST_C1, MOST_C2))
					msg(MOST_C2, u'Внимание! "%s" из  "%s" открыл мост между конференциями!  (закрыть мост можно по команде "мост_дел")' % (source[2], MOST_C1))
				else:
					reply(type, source, u'мост уже используеться '+MOST_C1+' & '+MOST_C2)
			else:
				reply(type, source, u'меня там нет!')
		else:
			reply(type, source, u'чего?')
	else:
		reply(type, source, u'эта команда выполняется только в чате!')

def handler_most_delete(type, source, body):
	if type != 'private' or handler_jid(source[0]) in ADLIST:
		if source[1] in [MOST_C1, MOST_C2]:
			msg(MOST_C1, u'Мост разорван!')
			globals()['MOST_C1'] = None
			msg(MOST_C2, u'Мост разорван!')
			globals()['MOST_C2'] = None
		else:
			reply(type, source, u'тут мост и не используется!')
	else:
		reply(type, source, u'эта команда выполняется только в чате!')

handler_register("01eh", most_message_handler)
handler_register("05eh", most_leave_handler)
handler_register("04eh", most_join_handler)
command_handler(handler_most_create, 30, "most")
command_handler(handler_most_delete, 20, "most")
