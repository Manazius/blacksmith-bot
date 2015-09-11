# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  newjid_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

LASTREG = 0

def handler_REGJID(User, Server, codename):
	cl = xmpp.Client(server = Server, port = PORT, debug = [])
	try:
		if not cl.connect(server = (Server, PORT), use_srv = False):
			return [False, 'None']
		try:
			REG = xmpp.features.register(cl, Server, {'username': User, 'password': codename})
		except:
			return [False, '0']
		try:
			Auth = cl.auth(User, codename, 'BS-BOT')
		except:
			Auth = False
		return [Auth, REG]
	finally:
		if cl.isConnected():
			try:
				cl.disconnect()
			except:
				pass

def handler_REGJID_command(type, source, body):
	timer = (time.time() - LASTREG)
	if timer >= 90:
		if body:
			list = body.split()
			if len(list) >= 2:
				aka = list[0].strip()
				if len(aka) <= 16:
					host = list[1].strip().lower()
					if len(list) >= 3:
						codename = list[2].strip()
						code_col = len(codename)
						if code_col < 8:
							codename = PASS_GENERATOR(codename, 8 - code_col)
						elif code_col > 64:
							codename = codename[:64]
					else:
						codename = PASS_GENERATOR('', 16)
					globals()['LASTREG'], REG = time.time(), handler_REGJID(aka, host, codename)
					if REG[0]:
						if REG[1]:
							reply(type, source, u'%s@%s успешно зарегистрирован!' % (aka, host))
						else:
							reply(type, source, u'По-моему, %s@%s уже был зареган, но мы вроде бы угадали с паролем :lol:' % (aka, host))
						msg(source[0], codename)
					elif REG[1] == 'None':
						reply(type, source, u'Нет соединения с указанным хостом!')
					elif REG[1] == '0':
						reply(type, source, u'Критическая ошибка регистрации!')
					elif REG[1]:
						reply(type, source, u'Не понятно, зарегал (%s@%s) или нет' % (aka, host))
						msg(source[0], codename)
					else:
						reply(type, source, u'Неудачная попытка регистрации...')
				else:
					reply(type, source, u'слишком длинный аккаунт!')
			else:
				reply(type, source, u'инвалид синтакс!')
		else:
			reply(type, source, u'чего хочешь то?')
	else:
		strtimer = str(round(90 - timer, 1))
		reply(type, source, u'Попробуй чуть позже (доступно через %s секунд)!' % (strtimer))

command_handler(handler_REGJID_command, 10, "newjid")
