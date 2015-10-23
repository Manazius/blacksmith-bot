# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  xboltun.py

#  Copyleft

#-extmanager-depends:static/boltun/ident_base.txt;static/boltun/random_base.txt-#
#-extmanager-extVer:1.5-#

IDENT_BASE = 'static/boltun/ident_base.txt'
RAND_BASE = 'static/boltun/random_base.txt'

BASE_LINES = 0

boltun_base = open(RAND_BASE, 'r')
while True:
	line = boltun_base.readline()
	if not line:
		break
	BASE_LINES += 1
boltun_base.close()

FLOOD = {}

def handler_get_reply(fraza):
	fi = open(IDENT_BASE, 'r')
	INFO['fr'] += 1
	while True:
		line = fi.readline()
		if not line:
			break
		base_fraza = unicode(line, 'utf-8')
		(key, otvet) = base_fraza.split(' = ', 1)
		key = key.strip().lower()
		if fraza.count(key):
			if otvet.count('/'):
				otvet = random.choice(otvet.split('/'))
			return otvet
	col, iters = random.randrange(1, BASE_LINES), 0
	fr = open(RAND_BASE, 'r')
	INFO['fr'] += 1
	while True:
		rand_base_fraza = fr.readline()
		iters += 1
		if iters >= col:
			return unicode(rand_base_fraza, 'utf-8')

def boltun_work(raw, type, source, body):
	if source[1] not in FLOOD or FLOOD[source[1]] != 'off':
		if 7 != random.randrange(1, 10):
			if Prefix_state(body, handler_botnick(source[1])) or type == 'private':
				reply(type, source, handler_get_reply(body.lower()))

def boltun_control(type, source, body):
	if source[1] in GROUPCHATS:
		if body:
			body = body.lower()
			filename = 'dynamic/%s/flood.txt' % (source[1])
			if body in [u'вкл', 'on', '1']:
				FLOOD[source[1]] = 'on'
				write_file(filename, "'on'")
				reply(type, source, u'болталка включена')
			elif body in [u'выкл', 'off', '0']:
				FLOOD[source[1]] = 'off'
				write_file(filename, "'off'")
				reply(type, source, u'болталка выключена')
			else:
				reply(type, source, u'читай помощь по команде')
		elif FLOOD[source[1]] == 'off':
			reply(type, source, u'сейчас болталка выключена')
		else:
			reply(type, source, u'сейчас болталка включена')
	else:
		reply(type, source, u'только в чате мудак!')

def boltun_work_init(conf):
	if check_file(conf, 'flood.txt', "'on'"):
		FLOOD[conf] = eval(read_file('dynamic/%s/flood.txt' % (conf)))
	else:
		FLOOD[conf] = 'on'
		delivery(u'Внимание! Не удалось создать flood.txt для "%s"!' % (conf))

handler_register("01eh", boltun_work)

command_handler(boltun_control, 20, "xboltun")

handler_register("01si", boltun_work_init)
