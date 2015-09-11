# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin

# Coded by: WitcherGeralt [WitcherGeralt@rocketmail.com]
# http://witcher-team.ucoz.ru/


def blacksmith_svn(type, source, body):
	if body:
		body, call, rlist = body.split(), 0, {}
		req = body[0].lower()
		if req in [u'ласт', 'last']:
			try:
				repl = u'Последнее доступное обновление BlackSmith — r%s' % re_search(read_link('http://blacksmith-bot.googlecode.com/svn/'), 'Revision', ': /')
			except:
				repl = u'Не достучался до репозитория.'
			reply(type, source, repl)
		elif req in [u'инфо', 'info']:
			if len(body) >= 2:
				call = body[1].strip()
				if check_number(call):
					call = int(call)
			try:
				lines = re_search(read_link('http://blacksmith-bot.googlecode.com/svn/tags/'), '<ul>', '</ul>').split('<li>')
				for line in lines:
					if line.strip():
						rev_html = re_search(line, '">', '</a>')
						if rev_html.count('-'):
							number = rev_html.split('-')[1].replace('.html', '')
							if check_number(number):
								rlist[int(number)] = rev_html
				if call:
					if call in [u'лист', 'list']:
						revision = -100
					elif rlist.has_key(call):
						revision = call
					else:
						revision = -200
				else:
					revision = max(rlist.keys())
				if revision == -100:
					revs = ", ".join(sorted([str(x) for x in rlist.keys()]))
					repl = u'Есть информация о ревизиях: %s' % (revs)
				elif revision == -200:
					repl = u'Нет инфы о такой ревизии…'
				else:
					repl = '\n'+uHTML(unicode(re_search(read_link('http://blacksmith-bot.googlecode.com/svn/tags/%s' % (rlist[revision])), '<div>', '</div>'), 'windows-1251'))
			except:
				print_exc()
				repl = u'Не достучался до репозитория.'
			reply(type, source, repl)
		elif req == u'обновление' and has_access(source[0], 100, source[1]):
			reply(type, source, u'%s\nПеред перезагрузкой обязательно проверьте совместимость (не изменился ли конфиг и т.п.) по команде "свн инфо".' % read_pipe("svn up"))
		else:
			reply(type, source, u'что?')
	else:
		reply(type, source, u'что?')

command_handler(blacksmith_svn, 11, "svn_info")
