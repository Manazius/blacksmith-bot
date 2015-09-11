# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  cipher_plugin.py

# Author: ferym (ferym@jabbim.org.ru)
# http://jabbrik.ru

strip_tags = re.compile(r'<[^<>]+>')

def handler_msk_time(type, source, body):
	try:
		body = re_search(read_url('http://www.zln.ru/time/', 'Mozilla/5.0'), '<div id="servertime" style="margin-top:40px; margin-bottom:30px; height:44px; padding:6px; width:148px; border:2px dotted #990000; font-size:36px; font-weight:bold;">', '</div>')
		body = strip_tags.sub('', replace_all(body, {'<br />': '', '<br>': ''}))
		day, mes, god, mes2, chas, minut, sek = time.strftime('%d.'), time.strftime('(%B)'), time.strftime('%Y'),time.strftime('%m.'), time.strftime('%H:'), time.strftime('%M:'), time.strftime('%S')
		week = [u'понедельник', u'вторник', u'среда', u'четверг', u'пятница', u'суббота', u'воскресенье']
		repl = u'Точное время:\n'
		repl += u'Время: %s' % (unicode(body, 'windows-1251'))
		repl += u'\nЧисло: %s' % (day)
		repl += u'(%s' % (week[time.localtime()[6]])
		repl += u')\nМесяц: %s' % (mes2+mes)
		repl += u'\nГод: %s' % (god)
		repl += u'\n-----'
		repl += u'\nВремя на локальном сервере: %s' % (chas+minut+sek)
		repl += u'\n-----'
		repl += u'\n[%s' % unicode(body, 'windows-1251')
		repl += u' %s' % (day+mes2+god)
		repl += u'] GMT +'
		repl += str(int(time.timezone)/int(3600))[1:]
		if time.localtime()[8] == 1:
			repl += u' (Летнее время)'
		else:
			repl += u' (Зимнее время)'
	except:
		repl = u'не вышло'
	reply(type, source, repl)

command_handler(handler_msk_time, 10, "networktime")
