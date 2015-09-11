# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  price_plugin.py

# Author: ferym (ferym@jabbim.org.ru)
# Ported from Isida by: WitcherGeralt (WitcherGeralt@jabber.ru)

def handler_price(type, source, body):
	if body:
		if not body.count('http://'):
			try:
				data = re_search(read_url('http://www.webvaluer.org/ru/www.%s' % (body.encode('utf-8')), 'Mozilla/5.0'), '<span style=\"color:green; font-weight:bold;\">', '</span></h1>')
				repl = unicode(data.replace(',', ''), 'UTF-8')
				respl = repl.split()
				if len(respl) >= 2:
					if respl[0] == u'руб':
						repl = u'%s рублей' % (respl[1].strip())
					else:
						repl = '%s %s' % (respl[1].strip(), respl[0].strip())
				reply(type, source, u'Примерная стоимость домена - %s' % (repl))
			except:
				reply(type, source, u'Не получилось обработать запрос')
		else:
			reply(type, source, u'формат ввода сайта; domain.tld')
	else:
		reply(type, source, u'а чё оценивать то?')

command_handler(handler_price, 10, "price")
