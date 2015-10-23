# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  boltun.py

#  Copyleft

#-extmanager-extVer:2.2-#

BOLTUN_FILE = 'dynamic/boltun.txt'

FLOOD = {}
FRAZA_BOT = {}
FRAZA_RANDOM = ['WTF?', 'How are you?', 'What the beatiful day!']
FRAZA_USER = {}
FRAZA_ALL = {}
 
def boltun_check_nick(item, conf):
	if conf in GROUPCHATS.keys():
		for nick in GROUPCHATS[conf].keys():
			if item.count(nick):
				return True
	return False

def boltun_talk(type, source, body, base):
	body = body.lower()
	for fr in base:
		if body.count(fr):
			reply(type, source, random.choice(base[fr]))
			return True
	return False

def boltun_work(raw, type, source, body):
	if source[1] not in FLOOD or FLOOD[source[1]] != 'off':
		if 7 != random.randrange(1, 10):
			if Prefix_state(body, handler_botnick(source[1])) or type == 'private':
				if not boltun_talk(type, source, body, FRAZA_BOT):
					reply(type, source, random.choice(FRAZA_RANDOM))
			elif type == 'public':
				if boltun_check_nick(body.split()[0].strip(), source[1]):
					boltun_talk(type, source, body, FRAZA_USER)
				else:
					boltun_talk(type, source, body, FRAZA_ALL)

def boltun_base_resave(key, list):
	BASE = eval(read_file(BOLTUN_FILE))
	BASE[key] = list
	write_file(BOLTUN_FILE, str(BASE))

def boltun_base(base, base_name, type, source, Params):
	body = Params.split()
	if len(body) >= 2:
		fraza = Params[(Params.find(' ') + 1):].strip()
		action = body[0].strip()
		if action == '+':
			args = fraza.split('=', 1)
			if len(args) == 2:
				if args[1].count('/'):
					key, items = args[0].strip().lower(), args[1].split('/')
					if key in base:
						for fr in items:
							base[key].append(fr)
					else:
						base[key] = (items)
					boltun_base_resave(base_name, base)
					reply(type, source, u'добавлено')
				else:
					reply(type, source, u'почитай-ка помощь по команде')
			else:
				reply(type, source, u'почитай-ка помощь по команде')
		elif action == '-':
			fraza = fraza.lower()
			if fraza in base:
				del base[fraza]
				boltun_base_resave(base_name, base)
				reply(type, source, u'удалено')
			else:
				reply(type, source, u'такой фразы в базе нет')
		elif action == '*':
			fraza = fraza.lower()
			if fraza in base:
				list, col = '', 0
				for fr in base[fraza]:
					col = col + 1
					list += '\n%d. %s' % (col, fr)
				reply(type, source, u'Всего фраз '+str(col)+':'+list)
			else:
				reply(type, source, u'такого ключа в базе нет')
		else:
			reply(type, source, u'почитай-ка помощь по команде')
	else:
		list, col = '', 0
		for fr in base:
			col = col + 1
			list += '\n%d. %s' % (col, fr)
		if col != 0:
			reply(type, source, u'Всего ключей '+str(col)+':'+list)
		else:
			reply(type, source, u'База пуста!')

def boltun_bot(type, source, Params):
	boltun_base(FRAZA_BOT, 'FRAZA_BOT', type, source, Params)

def boltun_rand(type, source, Params):
	body = Params.split()
	if len(body) >= 2:
		fraza = Params[(Params.find(' ') + 1):].strip()
		action = body[0].strip()
		if action == '+':
			fraza = fraza.lower()
			if fraza not in FRAZA_RANDOM:
				FRAZA_RANDOM.append(fraza)
				boltun_base_resave('FRAZA_RANDOM', FRAZA_RANDOM)
				reply(type, source, u'добавлено')
			else:
				reply(type, source, u'в базе уже есть такая фраза')
		elif action == '-':
			fraza = fraza.lower()
			if fraza in FRAZA_RANDOM:
				FRAZA_RANDOM.remove(fraza)
				boltun_base_resave('FRAZA_RANDOM', FRAZA_RANDOM)
				reply(type, source, u'удалено')
			else:
				reply(type, source, u'такой фразы в базе нет')
		else:
			reply(type, source, u'почитай-ка помощь по команде')
	else:
		list, col = '', 0
		for fr in FRAZA_RANDOM:
			col = col + 1
			list += '\n%d. %s' % (col, fr)
		reply(type, source, u'Всего фраз в базе '+str(col)+':'+list)

def boltun_user(type, source, Params):
	boltun_base(FRAZA_USER, 'FRAZA_USER', type, source, Params)

def boltun_all(type, source, Params):
	boltun_base(FRAZA_ALL, 'FRAZA_ALL', type, source, Params)

def boltun_base_export(name, list, type, source):
	col, text = 0, '\t\t%s' % (name)
	for key in sorted(list.keys()):
		col += 1
		text += '\n\n%d. %s:' % (col, key.encode('utf-8'))
		keys_col = 0
		for item in list[key]:
			keys_col += 1
			text += '\n\t%d. %s' % (keys_col, item.encode('utf-8'))
	filename = 'exported/%s.txt' % (name)
	if initialize_file(filename, text):
		reply(type, source, filename)
	else:
		reply(type, source, u'системная ошибка, не удалось создать файл')

def boltun_export(type, source, body):
	if body:
		body = body.lower()
		if body == u'бот':
			boltun_base_export('FRAZA_BOT', FRAZA_BOT, type, source)
		elif body == u'ранд':
			text, col = '\t\tFRAZA_RANDOM\n', 0
			for key in FRAZA_RANDOM:
				col += 1
				text += '\n%d. %s' % (col, key.encode('utf-8'))
			if initialize_file('exported/FRAZA_RANDOM.txt', text):
				reply(type, source, 'exported/FRAZA_RANDOM.txt')
			else:
				reply(type, source, u'системная ошибка, не удалось создать файл')
		elif body == u'юзер':
			boltun_base_export('FRAZA_USER', FRAZA_USER, type, source)
		elif body == u'чат':
			boltun_base_export('FRAZA_ALL', FRAZA_ALL, type, source)
		else:
			reply(type, source, u'бот, ранд, юзер, чат - остальное не нужно')
	else:
		reply(type, source, u'не врубаюсь чего ты хочешь')

def boltun_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/%s/flood.txt' % (source[1])
			if body in [u'вкл', 'on', '1']:
				FLOOD[source[1]] = 'on'
				write_file(filename, "'on'")
				reply(type, source, u'болталка включена')
			elif body in [u'выкл', 'off', '0']:
				FLOOD[source[1]] = 'off'
				write_file(filename, "'off'")
				reply(type, source, u'болталка выключена')
			else:
				reply(type, source, u'читай помощь по команде')
		elif FLOOD[source[1]] == 'off':
			reply(type, source, u'сейчас болталка выключена')
		else:
			reply(type, source, u'сейчас болталка включена')
	else:
		reply(type, source, u'только в чате!')

def boltun_file_init():
	if initialize_file(BOLTUN_FILE, str({'FRAZA_BOT': {}, 'FRAZA_RANDOM': FRAZA_RANDOM, 'FRAZA_USER': {}, 'FRAZA_ALL': {}})):
		base = eval(read_file(BOLTUN_FILE))
		globals()['FRAZA_BOT'] = base['FRAZA_BOT']
		globals()['FRAZA_RANDOM'] = base['FRAZA_RANDOM']
		globals()['FRAZA_USER'] = base['FRAZA_USER']
		globals()['FRAZA_ALL'] = base['FRAZA_ALL']
	else:
		Print('\n\nError: can`t create boltun.txt!', color2)

def boltun_work_init(conf):
	if check_file(conf, 'flood.txt', "'on'"):
		FLOOD[conf] = eval(read_file('dynamic/%s/flood.txt' % (conf)))
	else:
		FLOOD[conf] = 'on'
		delivery(u'Внимание! Не удалось создать flood.txt для "%s"!' % (conf))

handler_register("01eh", boltun_work)

command_handler(boltun_bot, 100, "boltun")
command_handler(boltun_rand, 100, "boltun")
command_handler(boltun_user, 100, "boltun")
command_handler(boltun_all, 100, "boltun")
command_handler(boltun_export, 100, "boltun")
command_handler(boltun_control, 20, "boltun")

handler_register("00si", boltun_file_init)
handler_register("01si", boltun_work_init)
