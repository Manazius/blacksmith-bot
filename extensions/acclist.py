# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  acclist_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def global_acclist(type, source, body):
	adminslist = u'Список администраторов:'
	ignorelist = u'Список игнора:'
	acclist = u'Остальные доступы:'
	col_1 = 0
	col_2 = 0
	col_3 = 0
	for jid in GLOBACCESS:
		access = GLOBACCESS[jid]
		if access >= 80:
			col_1 = col_1 + 1
			if access == 100:
				comment = ' - BOSS'
			elif access == 80:
				comment = ' - CHIEF'
			else:
				comment = ': '+str(access)
			adminslist += '\n'+str(col_1)+'. '+jid+comment
		elif access < 10:
			col_2 = col_2 + 1
			if access == -100:
				comment = u' - полный игнор'
			elif access == -5:
				comment = u' - заблокирован'
			else:
				comment = ': '+str(access)
			ignorelist += '\n'+str(col_2)+'. '+jid+comment
		else:
			col_3 = col_3 + 1
			acclist += '\n'+str(col_3)+'. '+jid+': '+str(access)
	if col_1 == 0:
		adminslist = u'Список администраторов пуст'
	if col_2 == 0:
		ignorelist = u'Список игнора пуст'
	if col_3 == 0:
		acclist = u'Нестандартных доступов нет'
	if type == 'public':
		reply(type, source, u'глянь в приват')
	reply('private', source, adminslist+'\n\n'+ignorelist+'\n\n'+acclist)

def local_acclist(type, source, body):
	if source[1] in GROUPCHATS:
		acclist = u'Список доступов:'
		ignorelist = u'Список игнора:'
		col_1 = 0
		col_2 = 0
		if source[1] in CONFACCESS:
			for jid in CONFACCESS[source[1]]:
				access = CONFACCESS[source[1]][jid]
				if access < 10:
					col_2 = col_2 + 1
					if access == -100:
						comment = u' - полный игнор'
					elif access == -5:
						comment = u' - заблокирован'
					else:
						comment = ': '+str(access)
					ignorelist += '\n'+str(col_2)+'. '+jid+comment
				else:
					col_1 = col_1 + 1
					if access == 100:
						comment = ' - BOSS'
					elif access == 80:
						comment = ' - CHIEF'
					else:
						comment = ': '+str(access)
					acclist += '\n'+str(col_1)+'. '+jid+comment
			if col_1 == 0:
				acclist = u'Список доступов пуст'
			if col_2 == 0:
				ignorelist = u'Список игнора пуст'
			if type == 'public':
				reply(type, source, u'глянь в приват')
			reply('private', source, acclist+'\n\n'+ignorelist)
		else:
			reply(type, source, u'нет локальных доступов')
	else:
		reply(type, source, u'какие ещё локальные доступы в ростере?')

command_handler(local_acclist, 20, "acclist")
command_handler(global_acclist, 80, "acclist")
