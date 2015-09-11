# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  access_plugin.py

# Author:
#  Mike Mintz [mikemintz@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

ACCESS_LIST = {'-100': u'(полный игнор)', '-5': u'(заблокирован)', '0': u'(никто)','1': '(lol)', '10': u'(юзер)', '11': u'(мембер)', '15': u'(модер)', '16': u'(модер)', '20': u'(админ)', '30': u'(овнер)', '80': '(CHIEF)', '100': '(BOSS)'}

def handler_superadmin_login(type, source, body):
	if body == BOSS_PASS:
		jid = handler_jid(source[0])
		if jid not in ADLIST:
			ADLIST.append(jid)
		GLOBACCESS[jid] = 100
		msg(BOSS, u"Внимание! \"%s\" из \"%s\" получил доступ 100 по команде \"логин\"." %\
			(handler_jid(source[0]), source[1]))
		reply(type, source, u'Стопудов! Ты верняк BOSS')
	else:
		reply(type, source, u'Пшёл вон, я хз кто ты!')
		msg(BOSS, u"Внимание! \"%s\" из \"%s\" пытается получить доступ 100 по команде \"логин\"." %\
			(handler_jid(source[0]), source[1]))

def handler_superadmin_logout(type, source, body):
	jid = handler_jid(source[0])
	if jid in ADLIST:
		ADLIST.remove(jid)
		del GLOBACCESS[jid]
		reply(type, source, u'Ну ладно, дело твоё...')
	else:
		reply(type, source, u'Пшел вон, ты и так не админ!')

def handler_view_access(type, source, body):
	if not body:
		level = str(user_level(source[0], source[1]))
		if level in ACCESS_LIST:
			levdesc = ' '+ACCESS_LIST[level]
		else:
			levdesc = ''
		reply(type, source, level+levdesc)
	elif body.lower() == u'инфо':
		reply('private', source, u'-100 - полный игнор, все сообщения от юзера с таким доступом будут пропускатся на уровне ядра\n-5 - заблокированный юзер (чаще всего автоблокировка за флуд атаку)\n0 - не может ничего, автоматически присваивается визиторам (visitor)\n10 - стандартный набор команд и макросов, автоматически присваивается партисипантам (participant)\n11 - стандартный набор команд и макросов, автоматически присваивается мемберам (member)\n15 (16) - модераторский набор команд и макросов, автоматически присваевается модераторам (moderator)\n20 - админский набор команд и макросов, автоматически присваивается админам (admin)\n30 - овнерский набор команд и макросов, автоматически присваиватся овнерам (owner)\n80 - доступ доверенному лицу\n100 - администратор бота, может всё')
	elif source[1] in GROUPCHATS:
		if body in GROUPCHATS[source[1]]:
			level = str(user_level(source[1]+'/'+body, source[1]))
			if level in ACCESS_LIST:
				levdesc = ' '+ACCESS_LIST[level]
			else:
				levdesc = ''
			reply(type, source, level+levdesc)
		else:
			reply(type, source, u'тут таких нет')
	else:
		reply(type, source, u'ты не в чате!')

def handler_set_access(type, source, Params):
	if source[1] in GROUPCHATS:
		if Params:
			splitdata = Params.split()
			if len(splitdata) <= 3:
				item = splitdata[0].strip()
				if len(splitdata) >= 2:
					access = splitdata[1].strip()
				elif len(splitdata) == 1:
					access = '0'
				if check_number(access):
					if item.count('@') and item.count('.'):
						jidto = item
					elif item in GROUPCHATS[source[1]]:
						jidto = handler_jid(source[1]+'/'+item)
					else:
						jidto = False
					if jidto:
						jidsource = handler_jid(source[0])
						accjidsource = user_level(source[0], source[1])
						accjidto = user_level(jidto, source[1])
						if jidsource not in ADLIST:
							if jidto == jidsource or accjidto >= accjidsource or int(access) >= accjidsource:
								has_acc = False
							else:
								has_acc = True
						else:
							has_acc = True
						if has_acc:
							if int(access) > 30:
								reply(type, source, u'больше 30 нельзя!')
							elif int(access) < -5:
								reply(type, source, u'меньше -5 нельзя!')
							elif access == '0':
								change_local_access(source[1], jidto)
								change_conf_access(source[1], jidto)
								reply(type, source, u'Кажись забрал доступ...')

							elif len(splitdata) == 1:
								if source[1] in CONFACCESS and jidto in CONFACCESS[source[1]]:
									change_conf_access(source[1], jidto)
								else:
									change_local_access(source[1], jidto)
								reply(type, source, u'снял доступ с "%s"' % (item))
							elif len(splitdata) == 2:
								change_local_access(source[1], jidto, int(access))
								reply(type, source, u'для "%s" дал временно доступ: %s' % (item, access))
							elif len(splitdata) == 3:
								change_conf_access(source[1], jidto, int(access))
								reply(type, source, u'для "%s" дал навсегда доступ: %s' % (item, access))
						else:
							reply(type, source, u'нет доступа!')
					else:
						reply(type, source, u'Это не жид, да и никого с таким ником я не знаю!')
				else:
					reply(type, source, u'Доступ, что ты пытаешься дать, не является числом!')
			else:
				reply(type, source, u'перебор параметров')
		else:
			reply(type, source, u'Чего ты от меня хочешь?')
	else:
		reply(type, source, u'ты не в чате!')

def handler_set_access_glob(type, source, Params):
	if Params:
		splitdata = Params.split()
		if len(splitdata) <= 2:
			item = splitdata[0].strip()
			if item.count('@') and item.count('.'):
				jid = item
			elif source[1] in GROUPCHATS and item in GROUPCHATS[source[1]]:
				jid = handler_jid(source[1]+'/'+item)
			else:
				jid = False
			if jid:
				if len(splitdata) == 2:
					access = splitdata[1].strip()
					if check_number(access):
						if access != '0':
							if jid not in ADLIST and int(access) >= 80:
								ADLIST.append(jid)
							change_global_access(jid, int(access))
							reply(type, source, u'Для "%s" установил доступ: %s' % (item, access))
						else:
							reply(type, source, u'Доступ "0" выдавать нельзя!')
					else:
						reply(type, source, u'Доступ что ты пытаешся дать не является числом!')
				elif len(splitdata) == 1:
					if jid in GLOBACCESS:
						if jid in ADLIST:
							ADLIST.remove(jid)
						change_global_access(jid)
						reply(type, source, u'Снял доступ c "%s"' % (item))
					else:
						reply(type, source, u'У "%s" и так нет глобального доступа!' % (item))
			else:
				reply(type, source, u'Это не жид да и никого с таким ником я незнаю!')
		else:
			reply(type, source, u'перебор параметров')
	else:
		reply(type, source, u'а дальше?')

def change_conf_access(conf, jid, level = 0):
	if conf not in CONFACCESS:
		CONFACCESS[conf] = {}
	if level:
		CONFACCESS[conf][jid] = level
	else:
		del CONFACCESS[conf][jid]
	write_file('dynamic/'+conf+'/access.txt', str(CONFACCESS[conf]))

def load_conf_access_levels(conf):
	if check_file(conf, 'access.txt'):
		CONFACCESS[conf] = eval(read_file('dynamic/'+conf+'/access.txt'))
	else:
		delivery(u'Внимание! Не удалось создать access.txt для "%s"!' % (conf))

if BOSS_PASS.strip():
	command_handler(handler_superadmin_login, 20, "access")

command_handler(handler_superadmin_logout, 20, "access")
command_handler(handler_view_access, 10, "access")
command_handler(handler_set_access, 20, "access")
command_handler(handler_set_access_glob, 100, "access")

handler_register("01si", load_conf_access_levels)
