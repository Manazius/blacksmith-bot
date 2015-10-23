# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  rss.py

# Copyright: Unknown author © ????
# Licensed under GPL v2 (as part of neutron-bot)
#-extmanager-extVer:1.1-# 

from xml.sax import make_parser, handler

RSS_CACHE_FILE = 'dynamic/RSS_CACHE.txt'
RSS_INTERVAL = 30
RSS_QUERY_DELAY = 10
RSS_ITEM_DELAY = 120

RSS_CONFS = {}
RSS_CACHE = {}
last_query = 0
UNSENT_HEADLINES = []

def rss_remove_html(body):
	EXP, list = re.compile('<[^>]*>'), {'&lt;p&gt;': '', '&lt;/p&gt;': '', '&lt;p /&gt;': '', '&lt;p/&gt;': '', '&lt;': '<', '&gt;': '>', '&amp;': '&', '&lt;': '<', '&gt;': '>', '&quot;': '"'}
	body = EXP.sub('', body)
	for symbol in list:
		body = body.replace(symbol, list[symbol])
	return body

def rss_update_file():
	write_file(RSS_CACHE_FILE, str(RSS_CACHE))

def rss_read_file():
	globals()['RSS_CACHE'] = eval(read_file(RSS_CACHE_FILE))

def rss_add_channel(name, url):
	if not RSS_CACHE.has_key(name):
		RSS_CACHE[name] = {'url': url, 'lastitem': '', 'subscribers': [], 'title': name, 'link': '', 'description': name}
		rss_update_file()
	else:
		RSS_CACHE[name]['url'] = url

def rss_remove_channel(name):
	if RSS_CACHE.has_key(name):
		del RSS_CACHE[name]
		rss_update_file()

def rss_subscribe(name, jid):
	if RSS_CACHE.has_key(name):
		if not jid in RSS_CACHE[name]['subscribers']:
			RSS_CACHE[name]['subscribers'].append(jid)
			rss_update_file()

def rss_unsubscribe(name, jid):
	if RSS_CACHE.has_key(name):
		if jid in RSS_CACHE[name]['subscribers']:
			RSS_CACHE[name]['subscribers'].remove(jid)
			rss_update_file()

def Conf_RSS(conf):
	while RSS_CONFS[conf]:
		rss_query_channels()
		time.sleep(RSS_ITEM_DELAY)
		if len(UNSENT_HEADLINES):
			random.shuffle(UNSENT_HEADLINES)
			(channel, item) = UNSENT_HEADLINES.pop()
			rss_dispatch_headline(channel, item)

def rss_query_channels():
	real_time = time.time()
	if real_time >= (last_query + (RSS_INTERVAL * 60)):
		globals()['last_query'] = real_time
		for channel in RSS_CACHE:
			rss_query_channel(channel)
			time.sleep(RSS_QUERY_DELAY)

def rss_query_channel(channel):
	parser = make_parser()
	parser.setContentHandler(RSSHandler(channel))
	try:
		parser.parse(RSS_CACHE[channel]['url'])
	except:
		LAST['null'] += 1

def rss_dispatch_headlines(channel, info, items):
	RSS_CACHE[channel]['title'] = info['title']
	RSS_CACHE[channel]['link'] = info['link']
	RSS_CACHE[channel]['description'] = info['description']
	for item in items:
		if item == RSS_CACHE[channel]['lastitem']:
			break
		else:
			UNSENT_HEADLINES.append((channel, item))
	RSS_CACHE[channel]['lastitem'] = items[0]
	rss_update_file()

def rss_dispatch_headline(channel, item):
	globaltitle = RSS_CACHE[channel]['title']
	title = rss_remove_html(item['title'])
	link = item['link']
	description = rss_remove_html(item['description'])
	reply = title+' - '
	if description:
		reply += description+' - '
	reply += link
	for conf in RSS_CACHE[channel]['subscribers']:
		if RSS_CONFS[conf]:
			msg(conf, reply)

class RSSHandler(handler.ContentHandler):
	def __init__(self, channel):
		handler.ContentHandler.__init__(self)
		self.channel = channel
		self.info = {'title': '', 'link': '', 'description': ''}
		self.items = []
		self._text = ''
		self._parent = None
		self._title = ''
		self._link = ''
		self._description = ''

	def startElement(self, name, attrs):
		if name in ['item', 'channel']:
			self._parent = name
		self._text = ''

	def endElement(self, name):
		if self._parent == 'channel':
			if name == 'title':
				self.info['title'] = self._text
			elif name == 'description':
				self.info['description'] = self._text
			elif name == 'link':
				self.info['link'] = self._text
		elif self._parent == 'item':
			if name == 'title':
				self._title = self._text
			elif name == 'link':
				self._link = self._text
			elif name == 'description':
				self._description = self._text
			elif name == 'item':
				self.items.append({'title': self._title, 'link': self._link, 'description': self._description})
				self._title = ''
				self._link = ''
				self._description = ''
		if name in ['rss', 'rdf:RDF']:
			rss_dispatch_headlines(self.channel, self.info, self.items)

	def characters(self, content):
		self._text = self._text+content

def handler_rss_control(type, source, body):
	if body:
		body = body.lower()
		if body in [u'старт', 'start']:
			if not RSS_CONFS.get(source[1], False):
				RSS_CONFS[source[1]] = True
				INFO['thr'] += 1
				try:
					threading.Thread(None, Conf_RSS, 'RSS-%d' % (INFO['thr']),(source[1],)).start()
				except:
					RSS_CONFS[source[1]] = False
				if RSS_CONFS[source[1]]:
					reply(type, source, 'Enabled RSS')
				else:
					reply(type, source, 'Can`t Enable RSS')
			else:
				reply(type, source, 'RSS is already Enabled')
		elif body in [u'стоп', 'stop']:
			RSS_CONFS[source[1]] = False
			reply(type, source, 'Disabled RSS')
		else:
			reply(type, source, 'Invalid Syntax')
	else:
		reply(type, source, 'Invalid Syntax')

def handler_rss_channels(type, source, body):
	if body:
		list = body.split()
		if len(list) >= 2:
			cmd = list[0].strip().lower()
			if cmd in [u'адд', '+']:
				Params = body[(body.find(' ') + 1):].strip()
				if len(Params.split()) >= 2:
					(Name, url) = Params.split()
					rss_add_channel(Name, url)
					reply(type, source, u'Добавил: %s - %s' % (Name, url))
				else:
					reply(type, source, 'Invalid Syntax')
			elif cmd in [u'дел', '-']:
				Name = list[1].strip()
				rss_remove_channel(Name)
				reply(type, source, u'Удалил: %s' % (Name))
			else:
				reply(type, source, 'Invalid Syntax')
		else:
			reply(type, source, 'Invalid Syntax')
	else:
		reply(type, source, 'Invalid Syntax')

def handler_rss_subscribe(type, source, body):
	if body:
		list = body.split()
		if len(list) == 2:
			Name, key = list[1].strip(), list[0].strip().lower()
			if key in [u'адд', '+']:
				rss_subscribe(Name, source[1])
				reply(type, source, 'Subscribed: %s to %s' % (source[1], Name))
			elif key in [u'дел', '-']:
				rss_unsubscribe(Name, source[1])
				reply(type, source, 'Unsubscribed: %s from %s' % (source[1], Name))
			else:
				reply(type, source, 'Invalid Syntax')
		else:
			reply(type, source, 'Invalid Syntax')
	else:
		reply(type, source, 'Invalid Syntax')

def handler_rss_info(type, source, name):
	if name:
		if name in RSS_CACHE.keys():
			try:
				info = '%s - %s - %s - %s' % (unicode(RSS_CACHE[name]['url']), unicode(RSS_CACHE[name]['title']), unicode(RSS_CACHE[name]['link']), unicode(RSS_CACHE[name]['description']))
			except:
				info = u'Это отличный канал с кучей полезной информации!'
			repl = '%s - %s - Subscribers: ' % (name, info)
			if RSS_CACHE[name]['subscribers']:
				repl += ', '.join(sorted(RSS_CACHE[name]['subscribers']))
			else:
				repl += 'NONE'
		else:
			repl = 'Этого канала нет в списке!'
	else:
		list, col = '', 0
		for channel in RSS_CACHE.keys():
			col = col + 1
			list += '\n'+str(col)+'. '+channel
		if col != 0:
			repl = u'Список каналов:'+list
		else:
			repl = u'В списке нет ни одного канала!'
	reply(type, source, repl)

def rss_file_init():
	if initialize_file(RSS_CACHE_FILE):
		rss_read_file()
	else:
		Print('\n\nError: can`t create RSS cache file!', color2)

command_handler(handler_rss_control, 30, "rss")
command_handler(handler_rss_channels, 100, "rss")
command_handler(handler_rss_subscribe, 30, "rss")
command_handler(handler_rss_info, 30, "rss")

handler_register("00si", rss_file_init)
