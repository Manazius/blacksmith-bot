# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  wtf_plugin.py

# Author:
#  Mike Mintz [mikemintz@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

WTF_FILE = 'dynamic/wtf.txt'

def handler_wtf_global(type, source, body):
	if body:
		args = body.split('=', 1)
		if len(args) == 2:
			try:
				globaldb = eval(read_file(WTF_FILE))
			except:
				globaldb = {}
			key, value = args[0].lower().strip(), args[1].strip()
			if not value:
				if globaldb.has_key(key):
					del globaldb[key]
					write_file(WTF_FILE, str(globaldb))
					reply(type, source, u'"%s" прибил нафиг!' % (key))
				else:
					reply(type, source, u'"%s" и так нет в базе!' % (key))
			else:
				globaldb[key] = value+' (from '+source[2]+')'
				write_file(WTF_FILE, str(globaldb))
				reply(type, source, u'Теперь буду занть что такое -> "%s"' % (key))
		else:
			reply(type, source, u'Ты определённо что-то забыл!')
	else:
		reply(type, source, u'Ты определённо что-то забыл!')

def handler_wtf_lokal(type, source, body):
	if body:
		if source[1] in GROUPCHATS:
			args = body.split('=', 1)
			if len(args) == 2:
				base = 'dynamic/'+source[1]+'/localdb.txt'
				try:
					globaldb = eval(read_file(WTF_FILE))
				except:
					globaldb = {}
				try:
					localdb = eval(read_file(base))
				except:
					localdb = {}
				key, value = args[0].lower().strip(), args[1].strip()
				if not globaldb.has_key(key):
					if not value:
						if localdb.has_key(key):
							del localdb[key]
							write_file(base, str(localdb))
							reply(type, source, u'"%s" прибил нафиг!' % (key))
						else:
							reply(type, source, u'"%s" итак нет в базе!' % (key))
					else:
						localdb[key] = value+' (from '+source[2]+')'
						write_file(base, str(localdb))
						reply(type, source, u'Теперь буду занть что такое -> "%s"' % (key))
				else:
					reply(type, source, u'"%s" уже есть в глобальной базе!' % (key))
			else:
				reply(type, source, u'Ты определённо что-то забыл!')
		else:
			reply(type, source, u'Эй! очнись! ты не в чате!')
	else:
		reply(type, source, u'Ты определённо что-то забыл!')

WTF_TIMES = {}

def wtf_timer(conf):
	if conf not in WTF_TIMES:
		WTF_TIMES[conf] = 0
	return WTF_TIMES[conf]

def handler_wtf_public(type, source, body):
	if body:
		if source[1] in GROUPCHATS:
			timer = (time.time() - wtf_timer(source[1]))
			if timer >= 15:
				base = 'dynamic/'+source[1]+'/localdb.txt'
				try:
					globaldb = eval(read_file(WTF_FILE))
				except:
					globaldb = {}
				try:
					localdb = eval(read_file(base))
				except:
					localdb = {}
				key = body.lower().strip()
				if globaldb.has_key(key):
					WTF_TIMES[source[1]] = time.time()
					reply(type, source, '### '+key+' :\n\n'+globaldb[key])
				elif localdb.has_key(key):
					WTF_TIMES[source[1]] = time.time()
					reply(type, source, '### '+key+' :\n\n'+localdb[key])
				else:
					reply(type, source, u'Я понятия не имею что такое "%s"' % (key))
			else:
				reply(type, source, u'Не сейчас! Повтори через %s секунд...' % str(round(15 - timer, 1)))
		else:
			reply(type, source, u'Ты забыл что ты не в чате?')
	else:
		reply(type, source, u'Ты определённо что-то забыл!')

def handler_wtf_private(type, source, body):
	if body:
		if source[1] in GROUPCHATS:
			timer = (time.time() - wtf_timer(source[1]))
			if timer >= 15:
				args = body.split()
				nick = args[0].strip()
				if handler_botnick(source[1]) != nick:
					if len(args) >= 3:
						sec_nick = args[1].strip()
						splitnick = nick+' '+sec_nick
					else:
						splitnick = False
					if nick in GROUPCHATS[source[1]]:
						ckey = body[(body.find(' ') + 1):].strip()
						tojid = source[1]+'/'+nick
					elif splitnick and splitnick in GROUPCHATS[source[1]]:
						ckey = body[(body.find(sec_nick) + (len(sec_nick) + 1)):].strip()
						tojid = source[1]+'/'+splitnick
					else:
						ckey = body
						tojid = source[0]
					base = 'dynamic/'+source[1]+'/localdb.txt'
					try:
						globaldb = eval(read_file(WTF_FILE))
					except:
						globaldb = {}
					try:
						localdb = eval(read_file(base))
					except:
						localdb = {}
					key = ckey.lower().strip()
					if globaldb.has_key(key):
						WTF_TIMES[source[1]] = time.time()
						if type == 'public':
							reply(type, source, u'Отправлено!')
						msg(tojid, '### '+key+' :\n\n'+globaldb[key])
					elif localdb.has_key(key):
						WTF_TIMES[source[1]] = time.time()
						if type == 'public':
							reply(type, source, u'Отправлено!')
						msg(tojid, '### '+key+' :\n\n'+localdb[key])
					else:
						reply(type, source, u'Я понятия не имею что такое "%s"' % (key))
				else:
					reply(type, source, u'Мне то оно зачем?')
			else:
				reply(type, source, u'Не сейчас! Повтори через %s секунд...' % str(round(15 - timer, 1)))
		else:
			reply(type, source, u'Ты забыл что ты не в чате?')
	else:
		reply(type, source, u'Ты определённо что-то забыл!')

def handler_wtf_search(type, source, body):
	if body:
		if source[1] in GROUPCHATS:
			base = 'dynamic/'+source[1]+'/localdb.txt'
			try:
				globaldb = eval(read_file(WTF_FILE))
			except:
				globaldb = {}
			try:
				localdb = eval(read_file(base))
			except:
				localdb = {}
			repl, global_list, local_list, text = '', [], [], body.lower()
			if len(globaldb) != 0:
				for key in globaldb.keys():
					if key.count(text):
						global_list.append(key)
				if len(global_list) != 0:
					repl += u'\nВсего '+str(len(global_list))+u' совпадений c глобальной базой:\n'+', '.join(global_list)
				else:
					repl += u'\nНет совпадений с глобальной базой'
			else:
				repl += u'\nГлобальная база пуста'
			if len(localdb) != 0:
				for key in localdb.keys():
					if key.count(text):
						local_list.append(key)
				if len(local_list) != 0:
					repl += u'\nВсего '+str(len(local_list))+u' совпадений c локальной базой:\n'+', '.join(local_list)
				else:
					repl += u'\n\nНет совпадений с локальной базой'
			else:
				repl += u'\n\nЛокальная база пуста'
			reply(type, source, repl)
		else:
			reply(type, source, u'Ты забыл что ты не в чате?')
	else:
		reply(type, source, u'И чего дальше?')

def handler_wtf_all(type, source, body):
	if source[1] in GROUPCHATS:
		base = 'dynamic/'+source[1]+'/localdb.txt'
		try:
			globaldb = eval(read_file(WTF_FILE))
		except:
			globaldb = {}
		try:
			localdb = eval(read_file(base))
		except:
			localdb = {}
		repl, global_col, global_list, local_col, local_list = '', 0, '', 0, ''
		for key in globaldb.keys():
			global_col += 1
			global_list += '\n'+str(global_col)+'. '+key
		if global_col != 0:
			repl += (u'\nВсего ключей в глобальной базе %s ключей:' % str(global_col))+global_list
		else:
			repl += u'\nГлобальная база пуста!'
		for key in localdb.keys():
			local_col += 1
			local_list += '\n'+str(local_col)+'. '+key
		if local_col != 0:
			repl += (u'\n\nВсего ключей в локальной базе %s ключей:' % str(local_col))+local_list
		else:
			repl += u'\n\nЛокальная база пуста!'
		reply(type, source, repl)
	else:
		reply(type, source, u'Ты забыл что ты не в чате?')

def handler_wtf_export(type, source, body):
	if body:
		body = body.lower()
		if body in [u'глоб', 'global']:
			base, name = WTF_FILE, 'exported/wtf_global.txt'
		elif body in GROUPCHATS:
			base = 'dynamic/'+body+'/localdb.txt'
			if check_nosimbols(body):
				name = 'exported/wtf_'+body+'.txt'
			else:
				name = 'exported/wtf_'+encode_name(body.encode('utf-8'))+'.txt'
		else:
			base = False
		if base:
			try:
				base = eval(read_file(base))
			except:
				base = {}
			text = ''
			for key in sorted(base.keys()):
				if text:
					text += '\n\n\n'
				text += '\t\t\t'+unicode(key).encode('utf-8')+'\n'+unicode(base[key]).encode('utf-8')
			if initialize_file(name, text):
				reply(type, source, name)
			else:
				reply(type, source, u'системная ошибка, не удалось создать файл')
		else:
			reply(type, source, u'Инвалид синтакс!')
	else:
		reply(type, source, u'И чего дальше?')

def global_wtf_file_init():
	if not initialize_file(WTF_FILE):
		Print('\n\nError: can`t create wtf.txt!', color2)

def lokal_wtf_file_init(conf):
	if not check_file(conf, 'localdb.txt'):
		delivery(u'Внимание! Не удалось создать localdb.txt для "%s"!' % (conf))

command_handler(handler_wtf_global, 100, "wtf")
command_handler(handler_wtf_lokal, 20, "wtf")
command_handler(handler_wtf_public, 10, "wtf")
command_handler(handler_wtf_private, 10, "wtf")
command_handler(handler_wtf_search, 10, "wtf")
command_handler(handler_wtf_all, 10, "wtf")
command_handler(handler_wtf_export, 100, "wtf")
handler_register("00si", global_wtf_file_init)

handler_register("01si", lokal_wtf_file_init)
