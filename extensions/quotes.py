# BS mark.1-55
# /* coding: utf-8 */
# © simpleApps, 2011 - 2013.


def AnecDote(mType, source, body):
	target = read_link("http://anekdot.odessa.ua/rand-anekdot.php")
	data = re.search(">(.*)<a href=", target, 16)
	if data:
		data = uHTML(data.group(1).decode("cp1251")).strip()
	reply(mType, source, u"Анекдот: \n%s" % data)

def bashOrg(type, source, body):
	if body.isdigit():
		link = "http://bash.im/quote/%s" % body
	else:
		link = "http://bash.im/random"
	data = read_url(link, UserAgents["BlackSmith"])
	try:
		data = re.search('<span id="v\d+?" class="rating">(\d+?)</span>(?:.|\s)+?<a href="/quote/\d+?" class="id">#(\d+?)</a>\s*?</div>\s+?<div class="text">((?:.|\s)+?)</div>', data, 16)
		if data:
			rate, id, data = data.groups()
			answer = uHTML(u"\nЦитата: #%s (Рейтинг: %s)\n%s" % (id, rate, data.decode("cp1251")))
		else:
			answer = u"Ошибка."
		reply(type, source, answer)
	except Exception:
		reply(type, source, returnExc())


def itHappens(mType, source, body):
	if body and body.isdigit():
		url = "http://ithappens.ru/story/%s" % body
	else:
		url = "http://ithappens.ru/random"
	data = read_url(url, UserAgents["BlackSmith"])
	data = re.search("<div class=\"text\">(.*)</p>", data, 16)
	if data:
		data = data.group(1).decode("cp1251")
		data = stripTags(uHTML(data), " ")
	reply(mType, source, data)


## by Snapi-Snup autor
def bashAbyss(mType, source, args):
	try:
		rawhtml = read_url('http://bash.im/abysstop', UserAgents["BlackSmith"])
		elements = re.findall("<div class=\"text\">(.+?)</div>", rawhtml, re.DOTALL)
		if elements:
			rawquote = random.choice(elements)
			message = "\n" + stripTags(uHTML(rawquote.decode("cp1251")))
		else:
			message = u"Что-то пусто..."
	except Exception:
		message = u"Что-то не так: %s" % str(returnExc())
	reply(mType, source, message)


def JQuotes(mType, source, body):
	if body and body.isdigit():
		url = "http://jabber-quotes.ru/api/read/?id=%d" % int(body)
	else:
		url = "http://jabber-quotes.ru/api/read/?id=random"
	data = read_url(url, UserAgents["BlackSmith"])
	data = re.search("<id>(.*)</id>\n<author>(.*)</author>\n<quote>(.*)</quote>", data, 16)
	if data:
		iD, Author, Quote = data.groups()
	reply(mType, source, "\nЦитата: #%s | Автор: %s.\n%s" % (iD, Author, uHTML(Quote)))

def pyOrg(type, source, body):
	if not body:
		try:
			data = re_search(read_link('http://python.org/'), '<h2 class="news">', '</div>')
			data, repl = stripTags(uHTML(data)), "\n"
			for line in data.splitlines():
				if line.strip():
					repl += '%s\n' % (line)
			reply(type, source, repl.decode('koi8-r'))
		except Exception:
			reply(type, source, returnExc())

def afor(type, source, body):
	try:
		data = re_search(read_url('http://skio.ru/quotes/humour_quotes.php',
			 UserAgents["BlackSmith"]), '<form id="qForm" method="post"><div align="center">', '</div>')
		data = stripTags(uHTML(data))
		reply(type, source, data.decode('cp1251'))
	except Exception:
		reply(type, source, returnExc())


def command_Chuck(mType, source, body):
	if body and check_number(body):
		Ask = "/quote/%d" % int(body)
	else:
		Ask = "/random"
	try:
		data = read_url("http://chucknorrisfacts.ru/%s" % Ask, UserAgents["BlackSmith"])
	except urllib2.HTTPError, exc:
		answer = str(exc)
	except:
		answer = u"Не могу получить доступ к странице."
	else:
		data = data.decode("cp1251")
		comp = re.compile("<a href=/quote/(\d+?)>.+?<blockquote>(.+?)</blockquote>", 16)
		data = comp.search(data)
		if data:
			answer = stripTags(uHTML(u"Факт #%s:\n%s" % data.groups()))
		else:
			answer = u"Проблемы с разметкой..."
	reply(mType, source, answer)

def getLinuxLink(mType, source, body):
	if not body:
		link = ""
		data = read_link("https://kernel.org")
		expression = re.search('<td id="latest_link">(.*?)</td>', data, 16)
		if expression:
			link = expression.group(1)
		ver = getTagData("a", link)
		link = "https://kernel.org/%s" % getTagArg("a", "href", link).lstrip("./")
		reply(mType, source, u"Последняя стабильная версия ядра Linux: %(ver)s | %(link)s" % vars())

command_handler(command_Chuck, 10, "quotes")
command_handler(JQuotes, 10, "quotes")
command_handler(pyOrg, 10, "quotes")
command_handler(bashOrg, 10, "quotes")
command_handler(itHappens, 10, "quotes")
command_handler(AnecDote, 10, "quotes")
command_handler(bashAbyss, 0, "quotes")
command_handler(afor, 10, "quotes")
command_handler(getLinuxLink, 10, "quotes")