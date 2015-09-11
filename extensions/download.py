# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  download_plugin.py

# Coded by: WitcherGeralt [WitcherGeralt@rocketmail.com]
# http://witcher-team.ucoz.ru/

def build_filename(DIR, name):
	name_ = '%s/%s' % (DIR, name)
	if not os.path.exists(name_):
		return name_
	name = 'copy_%s' % (name)
	return build_filename(DIR, name)

def download_handler(type, source, body):
	if body:
		DIR, list = "Downloads", body.split()
		if not os.path.exists(DIR):
			os.mkdir(DIR, 0755)
		link = list[0].strip()
		if len(list) >= 2:
			name = list[1].strip()
		else:
			names = link.split('/')
			name = names[len(names) - 1]
		reply(type, source, u'Ждите окончания загрузки %s\nЭто может занять несколько минут...' % (name))
		Jid = handler_jid(source[0])
		if Jid not in [BOSS, BOSS.lower()]:
			delivery(u'Внимание! Качаю --> %s' % (link))
		dname = build_filename(DIR, name)
		try:
			from urllib import urlretrieve
			downloaded = urlretrieve(link, dname)
			del urlretrieve
		except:
			downloaded = False
		if downloaded and os.path.exists(dname):
			if len(downloaded) >= 2:
				try:
					size = int(downloaded[1].get('Content-Length', '0'))
				except:
					size = 0
			else:
				size = 0
			if size:
				repl = u'Файл "%s" (%s) успешно скачан --> %s' % (name, byteFormat(size), dname)
			else:
				repl = u'Файл "%s" успешно скачан --> %s' % (name, dname)
			reply(type, source, repl)
		else:
			reply(type, source, u'не качается...')
	else:
		reply(type, source, u'чё качать то?')

command_handler(download_handler, 100, "download")
