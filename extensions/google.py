# BS mark.1-55
# /* coding: utf-8 */

#	BlackSmith plugin

#	© WitcherGeralt, 2012.

from urllib import urlencode
	
gCache = []

	
def command_google(mType, source, body):
	if body:
		if (chr(42) != body.strip()):
			Ask = urlencode({'q': body.encode('utf-8')})
			try:
				data = read_url("http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s" % Ask, UserAgents["BlackSmith"])
			except urllib2.HTTPError, exc:
				answer = str(exc)
			except:
				answer = u"Не могу получить доступ к странице."
			else:
				try:
					data = simplejson.loads(data)
				except:
					answer = u"Что-то не так..."
				else:
					try:
						list = data["responseData"]["results"]
						desc = list.pop(0)
					except LookupError:
						answer = u"Ничего не найдено..."
					else:
						#desc = list.pop(0)
						ls = []
						ls.append(desc.get("title", "").replace("<b>", u"«").replace("</b>", u"»"))
						ls.append(desc.get("content", ""))
						ls.append(desc.get("unescapedUrl", ""))
						answer = stripTags(uHTML(str.join(chr(10), ls)))
						if list:
							source_ = handler_jid(source[0])
							if source_:
								for ls in gCache:
									if ls[:2] == (source_, 1):
										gCache.pop(gCache.index(ls))
										break
								while len(gCache) >= 8:
									gCache.pop(0)
								gCache.append((source_, 1, list))
								answer += u"\n\n** Ещё %d результатов (командуй «гугл *»)." % len(list)
		else:
			source_ = handler_jid(source[1] + "/" + source[2])
			if source_:
				list = []
				for ls in gCache:
					if ls[:2] == (source_, 1):
						list = gCache.pop(gCache.index(ls))[2]
						break
				if list:
					desc = list.pop(0)
					ls = []
					ls.append(desc.get("title", ""))
					ls.append(desc.get("content", ""))
					ls.append(desc.get("unescapedUrl", ""))
					answer = stripTags(uHTML(str.join(chr(10), ls)))
					if list:
						gCache.append((source_, 1, list))
						answer += u"\n\n** Ещё %d результатов (командуй «гугл *»)." % len(list)
				else:
					answer = u"Твоих запросов нет в базе."
			else:
				answer = u"Не вижу твоего JID'а, поэтому не могу найти твоих запросов в базе."
	else:
		answer = u"Проблемы с разметкой..."
	reply(mType, source, answer)


command_handler(command_google, 10, "google")
