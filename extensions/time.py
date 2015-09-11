# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  time_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>
#  Modifications Copyright © 2007 dimichxp <dimichxp@gmail.com>

def handler_gettime_xep_disco(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			jid = source[1]+'/'+body
			if body in GROUPCHATS[source[1]]:
				if GROUPCHATS[source[1]][body].has_key('timexep'):
					if GROUPCHATS[source[1]][body]['timexep']:
						gettime_xep0202(type, source, jid, body)
						return
					else:
						gettime_xep0090(type, source, jid, body)
						return
			else:
				reply(type, source, u'Я его незнаю!')
				return
		else:
			jid = source[0]
			if GROUPCHATS[source[1]][source[2]].has_key('timexep'):
				if GROUPCHATS[source[1]][source[2]]['timexep']:
					gettime_xep0202(type, source, jid, source[2])
					return
				else:
					gettime_xep0090(type, source, jid, source[2])
					return
		iq = xmpp.Iq(to = jid, typ = 'get')
		INFO['outiq'] += 1
		iq.addChild('query', {}, [], xmpp.NS_DISCO_INFO)
		jClient.SendAndCallForResponse(iq, handler_gettime_xep_disco_answer, {'type': type, 'source': source, 'body': body, 'jid': jid})
	else:
		reply(type, source, u'Только в чате!')

def handler_gettime_xep_disco_answer(coze, res, type, source, body, jid):
		if res:
			if res.getType() == 'result':
				res = res.getQueryChildren()
				for x in res:
					att = x.getAttrs()
					if att.has_key('var'):
						att = att['var']
						if att == 'urn:xmpp:time':
							if body:
								GROUPCHATS[source[1]][body]['timexep'] = 1
							else:
								GROUPCHATS[source[1]][source[2]]['timexep'] = 1
							gettime_xep0202(type, source, jid, body)
							return
				if body:
					if body in GROUPCHATS[source[1]]:
						GROUPCHATS[source[1]][body]['timexep'] = 0
					else:
						reply(type, source, u'не таких тут')
						return
				else:
					if source[2] in GROUPCHATS[source[1]]:
						GROUPCHATS[source[1]][source[2]]['timexep'] = 0
					else:
						reply(type, source, u'не таких тут')
						return
				gettime_xep0090(type, source, jid, body)
			else:
				reply(type, source, u'не дискаверится')

def gettime_xep0090(type, source, jid, body = None):
	if body:
		nick = body
	else:
		nick = ''
	time_iq = xmpp.Iq(to = jid, typ = 'get')
	INFO['outiq'] += 1
	time_iq.addChild('query', {}, [], xmpp.NS_TIME)
	jClient.SendAndCallForResponse(time_iq, gettime_xep0090_answer, {'type': type, 'source': source, 'nick': nick})

def gettime_xep0090_answer(coze, res, nick, type, source):
		if res:
			if res.getType() == 'error':
				if nick:
					reply(type, source, u'его клиент не дружит с этим')
				else:
					reply(type, source, u'твой клиент не дружит с этим')
			elif res.getType() == 'result':
				time = ''
				props = res.getQueryChildren()
				for p in props:
					if p.getName() == 'display':
						time = p.getData()
				if time:
					if nick:
						reply(type, source, u'У "%s" сейчас %s' % (nick, time))
					else:
						reply(type, source, u'У тебя сейчас %s' % (time))

def gettime_xep0202(type, source, jid, body = None):
	if body:
		nick = body
	else:
		nick = ''
	time_iq = xmpp.Iq(to = jid, typ = 'get')
	INFO['outiq'] += 1
	time_iq.addChild('time', {}, [], 'urn:xmpp:time')
	jClient.SendAndCallForResponse(time_iq, gettime_xep0202_answer, {'type': type, 'source': source, 'nick': nick})

def gettime_xep0202_answer(coze, res, nick, type, source):
		if res:
			if res.getType() == 'error':
				if nick:
					reply(type, source, u'хехе, твой клиент не дружит с этим')
				else:
					reply(type, source, u'хехе, его клиент не дружит с этим')
			elif res.getType() == 'result':
				tzo = ''
				utc = ''
				props = res.getChildren()
				for p in props:
					tzo = p.getTagData('tzo')
					utc = p.getTagData('utc')
				if tzo and utc:
					try:
						[sign, tzh, tzm] = re.match('(\+|-)?([0-9]+):([0-9]+)', tzo).groups()
						[year, month, day, hours, minutes, seconds] = re.match('([0-9]+)-([0-9]+)-([0-9]+)T([0-9]+):([0-9]+):([0-9]+)', utc).groups()
					except:
						reply(type, source, u'не парсится')
						return
					if sign == '-':
						hours = int(hours) - int(tzh)
						minutes = int(minutes) - int(tzm)
					else:
						hours = int(hours) + int(tzh)
						minutes = int(minutes) + int(tzm)
					if hours >= 24:
						day = int(day) + 1
					while hours >= 24:
						hours = int(hours) - 24
					while minutes >= 60:
						minutes = int(minutes) - 60
					if len(str(hours)) == 1:
						hours = '0'+str(hours)
					if len(str(minutes)) == 1:
						minutes = '0'+str(minutes)
					if len(str(seconds)) == 1:
						seconds = '0'+str(seconds)
					time = str(hours)+':'+str(minutes)+':'+str(seconds)
					date = str(year)+'-'+str(month)+'-'+str(day)
					if nick:
						reply(type, source, u'У "%s" сейчас %s (%s)' % (nick, time, date))
					else:
						reply(type, source, u'У тебя сейчас %s (%s)' % (time, date))
				else:
					reply(type, source, u'твой клиент - глюк, инфы не хватает')

command_handler(handler_gettime_xep_disco, 10, "time")
