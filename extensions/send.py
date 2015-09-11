# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  send_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Help Copyright © 2007 dimichxp <dimichxp@gmail.com>

SEND_CACHE = {}

def handler_send_save(ltype, source, body):
	if source[1] in GROUPCHATS:
		args = body.split()
		if len(args) >= 2:
			date = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())
			fromnick = u'%s попросил (%s) меня передать тебе следующее:\n\n' % (source[2], date)
			nick = args[0].strip()
			body = body[(body.find(' ') + 1):].strip()
			if len(body) <= 1024:
				if nick == 'BOSS':
					jid = handler_jid(source[0])
					if jid in AMSGBL:
						reply(ltype, source, u'Тебе запрещено отсылать мессаги админу.')
					else:
						delivery(u'Сообщение от '+source[2]+' ('+jid+'): '+body)
						reply(type, source, u'сделано')
				elif handler_botnick(source[1]) != nick:
					if nick in GROUPCHATS[source[1]] and GROUPCHATS[source[1]][nick]['ishere']:
						reply(ltype, source, u'Он уже в чате.')
					else:
						if not nick in SEND_CACHE[source[1]]:
							SEND_CACHE[source[1]][nick] = []
						SEND_CACHE[source[1]][nick].append(fromnick+body)
						write_file('dynamic/'+source[1]+'/send.txt', str(SEND_CACHE[source[1]]))
						reply(ltype, source, u'Как зайдёт, передам.')
				else:
					reply(ltype, source, u'Себе передать?')
			else:
				reply(type, source, u'Слишком длинная мессага!')
		else:
			reply(ltype, source, u'ты определённо что-то забыл')
	else:
		reply(ltype, source, u'Мы не в чате.')

def handler_send_join(conf, nick, afl, role, status, text):
	if nick in SEND_CACHE[conf]:
		for body in SEND_CACHE[conf][nick]:
			msg(conf+'/'+nick, body)
		del SEND_CACHE[conf][nick]
		write_file('dynamic/'+conf+'/send.txt', str(SEND_CACHE[conf]))

def get_send_cache(conf):
	if check_file(conf, 'send.txt'):
		cache = eval(read_file('dynamic/'+conf+'/send.txt'))
	else:
		cache = {}
		delivery(u'Внимание! Не удалось создать send.txt для "%s"!' % (conf))
	SEND_CACHE[conf] = cache

handler_register("04eh", handler_send_join)
command_handler(handler_send_save, 10, "send")

handler_register("01si", get_send_cache)
