# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  cipher_plugin.py

# Author: ferym (ferym@jabbim.org.ru)
# http://jabbrik.ru
# ReCoded by: WitcherGeralt (WitcherGeralt@jabber.ru)

def command_cipher(type, source, body):
	if body:
		if len(body) >= 4 or len(body) <= 10:
			body = body.lower()
			try:
				data = read_url('http://combats.stalkers.ru/?a=analiz_nick&word=%s' % (body.encode('cp-1251')), UseAgents["BlackSmith"])
				repl = re_search(data, "<tr><td><div style='text-align:center;'><b>", '</b></div></td></tr></table><center>')
				repl = stripTags(replace_all(repl, {'<br />': '\n', '<br>': '\n'}))
				reply(type, source, repl.decode("cp1251"))
			except:
				reply(type, source, u'что-то сломалось...')
		else:
			reply(type, source, u'слово должно содержать от 4 до 10 букв')
	else:
		reply(type, source, u'а что расшифровать-то?')

command_handler(command_cipher, 10, "cipher")
