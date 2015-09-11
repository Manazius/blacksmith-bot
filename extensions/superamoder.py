# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  superamoder_plugin.py

# (c) simpleApps, 2011 — 2013

BossToModer_exc = []

def BossToModer_cfg(mType, source, args):
	if args:
		args = args.split()
		Del = args[0] == "-"
		if not GROUPCHATS.get(source[1]):
			answer = u"Только для конференций."
		else:
			chat = source[1] if ((len(args) == 1) or not has_access(source[0], 80, source[1])) else args[1] 
			if not GROUPCHATS.get(chat):
				answer = u"«%s» не находится в списке конференций. Для получения списка конференций используйте команду «чатлист»." % chat
			elif (chat in BossToModer_exc) and not Del:
				answer = u"«%s» уже находится в списке исключений." % chat
			elif (chat not in BossToModer_exc) and Del:
				answer = u"«%s» не находится в списке исключений..." % chat
			else:
				exec ("BossToModer_exc.%s(chat)" % ("append", "remove")[Del])
				answer = u"Теперь суперадмин %s автоматически получать модератора в «%s»." % ((u"не будет", u"будет")[Del], chat) 
				write_file("dynamic/btm.txt", str(BossToModer_exc))
	else:
		if BossToModer_exc:
			answer = u"\n*** Список конференций, где суперадмин не будет модератором:\n"
			for x, y in enumerate(BossToModer_exc, 1):
				if y in GROUPCHATS:
					answer +=  u"%i. %s.\n" % (x, y)
				else:
					BossToModer_exc.remove(y)
		else:
			answer = u"0 ключей."
	reply(mType, source, answer)

def BossToModer_init(conf):
	if check_file(None, 'btm.txt', `[]`):
		chats = eval(read_file('dynamic/btm.txt'))
	else:
		chats = []
	globals()["BossToModer_exc"] = chats
	
def setBossToModer(conf, nick, afl, role, status, text):
	if not role == 'moderator':
		jid = handler_jid(conf+'/'+nick)
		if jid in ADLIST and not conf in BossToModer_exc:
			moderator(conf, nick, u'BOSS BlackSmith всегда модер!')

def superamoder_04si(chat):
	if chat in BossToModer_exc:
		BossToModer_exc.remove(chat)

command_handler(BossToModer_cfg, 30, "superamoder")
handler_register("04eh", setBossToModer)
handler_register("01si", BossToModer_init)
handler_register("04si", superamoder_04si)