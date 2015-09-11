# BS mark.1-55
# /* coding: utf8 */
# BlackSmith Bot Plugin
# © simpleApps Unofficial.

Langs = {'en': u'Английский',
			'ja': u'Японский',
			'ru': u'Русский',
			'auto': u'Авто',
			'sq': u'Албанский',
#			'ar': u'Арабский',
			'af': u'Африкаанс',
			'be': u'Белорусский',
			'bg': u'Болгарский',
			'cy': u'Валлийский',
			'hu': u'Венгерский',
			'vi': u'Вьетнамский',
			'gl': u'Галисийский',
			'nl': u'Голландский',
			'el': u'Греческий',
			'da': u'Датский',
			'iw': u'Иврит',
			'yi': u'Идиш',
			'id': u'Индонезийский',
			'ga': u'Ирландский',
			'is': u'Исландский',
			'es': u'Испанский',
			'it': u'Итальянский',
			'ca': u'Каталанский',
			'zh-CN': u'Китайский',
			'ko': u'Корейский',
			'lv': u'Латышский',
			'lt': u'Литовский',
			'mk': u'Македонский',
			'ms': u'Малайский',
			'mt': u'мальтийский',
			'de': u'Немецкий',
			'no': u'Норвежский',
			'fa': u'Персидский',
			'pl': u'Польский',
			'pt': u'Португальский',
			'ro': u'Румынский',
		 	'sr': u'Сербский',
		 	'sk': u'Словацкий',
		 	'sl': u'Словенский',
		 	'sw': u'Суахили',
		 	'tl': u'Тагальский',
		 	'th': u'Тайский',
		 	'tr': u'Турецкий',
		 	'uk': u'Украинский',
		 	'fi': u'Финский',
		 	'fr': u'Французский',
		 	'hi': u'Хинди',
		 	'hr': u'Хорватский',
		 	'cs': u'Чешский',
		 	'sv': u'Шведский',
		 	'et': u'Эстонский'}

import re
from urllib2 import quote

def gTrans(fLang, tLang, text):
	url = "http://translate.google.ru/m?hl=ru&sl=%(fLang)s&tl=%(tLang)s&ie=UTF-8&prev=_m&q=%(text)s"
	text = quote(text.encode("utf-8"))
	try:
		html = read_url(url % vars(), UserAgents["OperaMini"])
		return uHTML(re_search(html, 'class="t0">', "</div>"))
	except Exception, e:
		return "%s: %s" % (e.__class__.__name__, e.message)

def gAutoTrans(mType, source, text):
	if text:
		repl = gTrans("auto", "ru", text)
		if text == repl:
			repl = u"Перевод %s => %s:\n%s" % ("auto", "en", gTrans("auto", "en", text))
		else:
			repl = u"Перевод %s => %s:\n%s" % ("auto", "ru", repl)
	else:
		repl = u"Недостаточно параметров."
	reply(mType, source, repl)

def gTransHandler(mType, source, args):
	if args and len(args.split()) > 2:
		(fLang, tLang, text) = args.split(None, 2)
		reply(mType, source, u"Перевод %s => %s:\n%s" % (fLang, tLang, gTrans(fLang, tLang, text)))
	else:
		answer = u"\nДоступные языки:\n"
		for a, b in enumerate(sorted([x + u" — " + y for x, y in Langs.iteritems()])):
			answer += u"%i. %s.\n" % (a + 1, b)
		reply(mType, source, answer.encode("utf-8"))

command_handler(gTransHandler, 10, "trans")
command_handler(gAutoTrans, 10, "trans")
