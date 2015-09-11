# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  userch_plugin.py

# Idea: Gigabyte
# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)

def handler_usearch(type, source, object):
	if object:
		stalker = handler_jid(source[0])
		list, col = '', 0
		for conf in GROUPCHATS.keys():
			for usr in GROUPCHATS[conf]:
				jid = handler_jid(conf+'/'+usr)
				if jid.count(object) or usr.count(object):
					col = col + 1
					list += '\n'+str(col)+'. '+usr+' ('+conf+')'
					if stalker in ADLIST:
						list += ' ('+jid+')'
		if col != 0	:
			if type == 'public':
				reply(type, source, u'глянь в приват')
			reply('private', source, (u'Всего найдено %s совпадений:' % str(col))+list)
		else:
			reply(type, source, u'По запросу ничего не найдено')
	else:
		reply(type, source, u'Ничего не забыл?')

command_handler(handler_usearch, 10, "userch")
