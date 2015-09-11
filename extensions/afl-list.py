# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  afl-list_plugin.py

# Coded by: 40tman (40tman@qip.ru)
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)

AFLIST_SEARCH = {}

def get_afl_hnd(body):
	list = {u'овнер': 'owner', u'админ': 'admin', u'мембер': 'member', u'бан': 'outcast'}
	for afl in list.keys():
		if body.count(afl):
			return list[afl]
	return None

def handler_afl_list(type, source, body):
	if GROUPCHATS.has_key(source[1]):
		if body:
			body = body.lower()
			list = body.split()
			if list[0] in [u'искать', 'search']:
				if len(list) >= 2:
					id = '%s-%s' % (source[0], str(time.time()))
					AFLIST_SEARCH[id] = {}
					for afl in ['owner', 'admin', 'member', 'outcast']:
						iq = xmpp.Iq(to = source[1], typ = 'get')
						INFO['outiq'] += 1
						iq.setID('list_'+str(INFO['outiq']))
						query = xmpp.Node('query')
						query.setNamespace(xmpp.NS_MUC_ADMIN)
						query.addChild('item', {'affiliation': afl})
						iq.addChild(node = query)
						jClient.SendAndCallForResponse(iq, list_search_answer, {'id': id, 'afl': afl, 'name': list[1]})
					reply(type, source, u'Ответ ожидай в привате через ~32 секунды.')
					time.sleep(32)
					answer = ''
					for x in AFLIST_SEARCH[id].keys():
						if AFLIST_SEARCH[id][x]:
							answer += '\n%s:' % (x.upper())
							col = 0
							for y in AFLIST_SEARCH[id][x]:
								col += 1
								answer += '\n%d. %s' % (col, y)
					del AFLIST_SEARCH[id]
					if answer:
						msg(source[0], answer)
					else:
						reply(type, source, u'Ничего не найдено :(.')
				else:
					reply(type, source, u'инвалид синтакс')
			else:
				afl = get_afl_hnd(body)
				if afl:
					iq = xmpp.Iq(to = source[1], typ = 'get')
					INFO['outiq'] += 1
					iq.setID('list_'+str(INFO['outiq']))
					query = xmpp.Node('query')
					query.setNamespace(xmpp.NS_MUC_ADMIN)
					query.addChild('item', {'affiliation': afl})
					iq.addChild(node = query)
					jClient.SendAndCallForResponse(iq, handler_list_answer, {'type': type, 'source': source, 'afl': afl})
				else:
					reply(type, source, u'Что-что?')
		else:
			reply(type, source, u'Что-то не то...')
	else:
		reply(type, source, u'Мы не в чате!')

def list_search_answer(coze, stanza, id, afl, name):
	if AFLIST_SEARCH.has_key(id):
		AFLIST_SEARCH[id][afl] = []
		if stanza:
			if stanza.getType() == 'result':
				MASS = stanza.getChildren()
				if MASS:
					for item in MASS[0].getChildren():
						if item and item != 'None':
							jid = item.getAttrs()['jid']
							if jid and jid.count(name):
								try:
									AFLIST_SEARCH[id][afl].append(jid)
								except:
									break

def handler_list_answer(coze, stanza, type, source, afl):
	if stanza:
		if stanza.getType() == 'result':
			MASS = stanza.getChildren()
			if MASS:
				list = u'Список %s:' % (afl)
				col = 0
				for item in MASS[0].getChildren():
					if item and item != 'None':
						jid = item.getAttrs()['jid']
						if jid:
							col += 1
							if afl == 'outcast':
								if jid in ADLIST:
									none(source[1], jid)
							list += '\n'+str(col)+'. '+jid
							reasonTag = item.getTag("reason")
							if reasonTag:
								reason = reasonTag.getData()
								if reason:
									list += ' [%s]' % reason
				if col != 0:
					if type == 'public':
						reply(type, source, u'глянь в приват')
					reply('private', source, list)
				else:
					reply(type, source, u'Пусто.')
			else:
				reply(type, source, u'Что-то не вышло...')
		else:
			reply(type, source, u'Не судьба :(.')
	else:
		reply(type, source, u'Что-то не вышло.')

command_handler(handler_afl_list, 20, "afl-list")
