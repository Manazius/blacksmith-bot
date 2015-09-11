# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  verification_plugin.py
#  Ver.3.5

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

OTVET = {}
VERON = {}

def handler_verification(conf, nick, afl, role, status, text):
	if VERON[conf] != 'off' and afl == 'none':
		jid = handler_jid(conf+'/'+nick)
		if jid not in ADLIST:
			if not conf in OTVET:
				OTVET[conf] = {}
			QA = random.choice(QUESTIONS.keys())
			OTVET[conf][jid] = {'ansver': QUESTIONS[QA]['answer'], 'col': 0}
			visitor(conf, nick, u'%s: Авторизация...' % (handler_botnick(conf)))
			msg(conf+'/'+nick, u'Привет! Это IQ проверка, чтобы получить голос %s, у тебя три попытки!' % (QUESTIONS[QA]['question']))

def handler_verification_answer(raw, type, source, body):
	if type == 'private' and source[1] in VERON:
		if VERON[source[1]] != 'off' and source[1] in OTVET:
			jid = handler_jid(source[0])
			if jid in OTVET[source[1]]:
				if OTVET[source[1]][jid]['ansver'] == body.lower():
					del OTVET[source[1]][jid]
					participant(source[1], source[2], u'Авторизация пройдена!')
					reply(type, source, u'Ок, признаю - ты не бот')
				elif OTVET[source[1]][jid]['col'] >= 3:
					del OTVET[source[1]][jid]
					kick(source[1], source[2], u'%s: Не прошел авторизацию!' % (handler_botnick(source[1])))
				else:
					OTVET[source[1]][jid]['col'] += 1
					reply(type, source, u'Включи мозг! Неправильно!')

def handler_verification_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/'+source[1]+'/verification.txt'
			if body in [u'вкл', 'on', '1']:
				VERON[source[1]] = 'on'
				write_file(filename, "'on'")
				reply(type, source, u'авторизация включена')
			elif body in [u'выкл', 'off', '0']:
				VERON[source[1]] = 'off'
				write_file(filename, "'off'")
				reply(type, source, u'авторизация выключена')
			else:
				reply(type, source, u'читай помощь по команде')
		else:
			if VERON[source[1]] == 'off':
				reply(type, source, u'сейчас авторизация выключена')
			else:
				reply(type, source, u'сейчас авторизация включена')
	else:
		reply(type, source, u'только в чате мудак!')

def verification_init(conf):
	if check_file(conf, 'verification.txt', "'off'"):
		state = eval(read_file('dynamic/'+conf+'/verification.txt'))
	else:
		state = 'off'
		delivery(u'Внимание! Не удалось создать verification.txt для "%s"!' % (conf))
	VERON[conf] = state

handler_register("04eh", handler_verification)
handler_register("01eh", handler_verification_answer)
command_handler(handler_verification_control, 20, "verification")

handler_register("01si", verification_init)
