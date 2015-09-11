# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  antispace_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_antispace(Prs):
	chat = Prs.getFrom().getStripped()
	if chat in Antispace:
		code = Prs.getStatusCode()
		if code == '303':
			nick = Prs.getNick()
		else:
			nick = Prs.getFrom().getResource()
		if nick.endswith(chr(32)):
			kick(chat, nick, u'Пробелы в нике запрещены!')

def handler_antispace_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/antispace.txt'
			if body in (u'вкл', '1') and source[1] not in Antispace:
				Antispace.append(source[1])
				write_file(filename, str(Antispace))
				reply(type, source, u'Теперь включено.')
			elif body in (u'выкл', '0') and source[1] in Antispace:
				Antispace.remove(source[1])
				write_file(filename, str(Antispace))
				reply(type, source, u'Выключил.')
			else:
				reply(type, source, u'Либо что-то не то с параметрами, либо «антиспейс» уже имеет такое значение.')
		elif source[1] in Antispace:
			reply(type, source, u'Включено.')
		else:
			reply(type, source, u'Не включено.')
	else:
		reply(type, source, u'Только для чатов!')

def antispace_init():
	if initialize_file("dynamic/antispace.txt", "[]"):
		globals()["Antispace"] = eval(read_file('dynamic/antispace.txt'))
	else:
		globals()["Antispace"] = []
		delivery(u'Внимание! Не удалось создать antispace.txt!')

command_handler(handler_antispace_control, 20, "antispace")
handler_register("02si", antispace_init)
handler_register("02eh", handler_antispace)