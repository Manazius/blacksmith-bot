# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  absurd_plugin.py

# Author: ferym (ferym@jabbim.org.ru)
# http://jabbrik.ru
# ReCoded by: WitcherGeralt (WitcherGeralt@jabber.ru)

def handler_absurd(type, source, body):
	if body:
		try:
			data = read_url('http://absurdopedia.wikia.com/wiki/%s' % ((body.replace(' ', '_')).encode('utf-8')), 'Mozilla/5.0')
			data = re_search(data, '<meta name="description" content="', '" />')
			data = replace_all(data, {'<': '', '" target="_blank">': '\n', '>': ' ', '&': '', '_': '', '#': ''})
			reply(type, source, unicode(data, 'UTF-8'))
		except:
			reply(type, source, u'По вашему запросу ничего не найдено')
	else:
		reply(type, source, u'а что искать то?')

command_handler(handler_absurd, 10, "absurd")
