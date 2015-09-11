# BS mark.1-55
# /* coding: utf-8 */

#	© WitcherGeralt, 2012.

def command_YandexMarket(mType, source, body):
	if body:
		ls = body.split()
		c1st = (ls.pop(0)).lower()
		if check_number(c1st):
			if ls:
				c2st = ls.pop(0)
				if check_number(c2st):
					try:
						print c2st
						data = read_url("http://m.market.yandex.ru/spec.xml?hid=%d&modelid=%d" % (int(c1st), int(c2st)), UserAgents["OperaMini"])
					except urllib2.HTTPError, exc:
						answer = str(exc)
					except:
						answer = u"Не могу получить доступ к странице."
					else:
						data = data.decode("utf-8")
						data = re_search(data, "<h2 class=\"b-subtitle\">", "</div>")
						if data:
							data = data.replace("<li>", chr(10)).replace("<h2 class=\"b-subtitle\">", chr(10)*2).replace("</h2>", chr(10))
							answer = stripTags(data)
						else:
							answer = "Ничего не найдено..."
				else:
					answer = "Это не число."
			else:
				answer = "Инвалид синтакс."
		else:
			Req = (body if chr(42) != c1st else body[2:].strip())
			if Req:
				Req = urllib.quote_plus(Req.encode("utf-8"))
				try:
					data = read_url("http://m.market.yandex.ru/search.xml?nopreciser=1&text=%s" % Req, UserAgents["BlackSmith"])
				except urllib2.HTTPError, exc:
					answer = str(exc)
				except:
					answer = "Не могу получить доступ к странице."
				else:
					data = data.decode("utf-8")
					comp = re.compile("<a href=\"http://m\.market\.yandex\.ru/model\.xml\?hid=(\d+?)&amp;modelid=(\d+?)&amp;show-uid=\d+?\">(.+?)</a>", 16)
					list = comp.findall(data)
					if list:
						Number = 0
						ls = ["\n[#] [Name] (hid & ID)"]
						for hid, modelid, name in list:
							if not name.startswith("<img"):
								Number += 1
								ls.append("%d) %s (%s %s)" % (Number, uHTML(name), hid, modelid))
						answer = str.join(chr(10), ls)
					else:
						answer = "Ничего не найдено..."
			else:
				answer = "Инвалид синтакс."
	else:
		answer = "Данная команда подразумевает использование параметров."
	if locals().has_key("answer"):
		reply(mType, source, u"%s\n*** Информация предоставлена сервисом market.yandex.ru" % answer)

command_handler(command_YandexMarket, 10, "yandexmarket")