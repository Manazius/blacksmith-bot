# BS mark.1-55
# /* coding: utf-8 */

#	BlackSmith plugin

#	© WitcherGeralt, 2010-2013.


chat_file = lambda chat, name: "dynamic/%s/%s" % (chat, name)

UstatsFile = "jstat.db"

UstatsDesc = {}

# spike:

DeprecatedUstatsFile = "userstat.txt"

def user_stats_spike(conf, db):
	filename = chkFile(chat_file(conf, DeprecatedUstatsFile))
	if os.path.isfile(filename):
		try:
			stats = eval(read_file(filename))
		except MemoryError:
			pass
		else:
			for user, info in stats.iteritems():
				if info["joins"] > 2:
					db("insert into stat values (?,?,?,?,?,?,?)", (user, "%s/%s" % (info["afl"], info["role"]), info["joined"], info["joins"], info["seen"], info["leave"], "-/-".join(info["nicks"])))
			db.commit()
		os.remove(filename)

# end

def command_user_stats(stype, source, body):
	if source[1] in GROUPCHATS:
		if not body:
			body = handler_jid("%s/%s" % (source[1], source[2]))
		elif body in GROUPCHATS[source[1]]:
			body = handler_jid("%s/%s" % (source[1], body))
		filename = chkFile(chat_file(source[1], UstatsFile))
		with UstatsDesc[source[1]]:
			with database(filename) as db:
				db("select * from stat where jid=?", (body,))
				db_desc = db.fetchone()
		if db_desc:
			answer = u"\nВсего входов - %d\nВремя последнего входа - %s\nПоследняя роль - %s" % (db_desc[3], db_desc[2], db_desc[1])
			if db_desc[3] >= 2 and db_desc[4]:
				answer += u"\nВремя последнего выхода - %s\nПричина выхода - %s" % (db_desc[4], db_desc[5])
			answer += u"\nНики: %s" % (", ".join(sorted(db_desc[6].split("-/-"))))
		else:
			answer = u"Нет статистики."
	else:
		answer = u"Только для чатов."
	reply(stype, source, answer)

def command_here(stype, source, nick):
	if source[1] in GROUPCHATS:
		Chat = GROUPCHATS[source[1]]
		if not nick:
			nick = source[2]
		if nick in Chat and Chat[nick]["ishere"]:
			jtc = timeElapsed(time.time() - Chat[nick]["joined"])
			if nick != source[2]:
				answer = u"«%s» сидит здесь %s." % (nick, jtc)
			else:
				answer = u"Ты провёл здесь %s." % (jtc)
		else:
			answer = u"«%s» сейчас нет в чате." % (nick)
	else:
		answer = u"Только для чатов."
	reply(stype, source, answer)

def calc_stat_04eh(conf, nick, aff, role, *args):
	if nick != handler_botnick(conf):
		source_ = handler_jid("%s/%s" % (conf, nick))
		if source_:
			date = time.strftime("%d.%m.%Y (%H:%M:%S)", time.gmtime())
			filename = chkFile(chat_file(conf, UstatsFile))
			with UstatsDesc[conf]:
				with database(filename) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						db("update stat set joined=?, joins=? where jid=?", (date, (db_desc[3] + 1), source_))
						if nick not in db_desc[6].split("-/-"):
							db("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_desc[6], nick), source_))
						arole = "%s/%s" % (aff, role)
						if db_desc[1] != arole:
							db("update stat set arole=? where jid=?", (arole, source_))
						db.commit()
					else:
						db("insert into stat values (?,?,?,?,?,?,?)", (source_, "%s/%s" % (aff, role), date, 1, "", "", nick))
						db.commit()

def calc_stat_05eh(conf, nick, sbody, scode):
	if nick != handler_botnick(conf):
		source_ = handler_jid("%s/%s" % (conf, nick))
		if source_:
			sbody = unicode(sbody)
			if scode == "301":
				sbody = "banned:(%s)" % (sbody)
			elif scode == "307":
				sbody = "kicked:(%s)" % (sbody)
			date = time.strftime("%d.%m.%Y (%H:%M:%S) GMT", time.gmtime())
			filename = chkFile(chat_file(conf, UstatsFile))
			with UstatsDesc[conf]:
				with database(filename) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						db("update stat set seen=?, leave=? where jid=?", (date, sbody, source_))
						db.commit()

def calc_stat_06eh(node, conf, old_nick, nick):
	if nick != handler_botnick(conf):
		source_ = handler_jid("%s/%s" % (conf, nick))
		if source_:
			filename = chkFile(chat_file(conf, UstatsFile))
			with UstatsDesc[conf]:
				with database(filename) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc and nick not in db_desc[6].split("-/-"):
						db("update stat set nicks=? where jid=?", ("%s-/-%s" % (db_desc[6], nick), source_))
						db.commit()

def calc_stat_07eh(conf, nick, role, reason):
	if nick != handler_botnick(conf):
		source_ = handler_jid("%s/%s" % (conf, nick))
		if source_:
			filename = chkFile(chat_file(conf, UstatsFile))
			with UstatsDesc[conf]:
				with database(filename) as db:
					db("select * from stat where jid=?", (source_,))
					db_desc = db.fetchone()
					if db_desc:
						arole = "{1}/{0}".format(*role)
						if db_desc[1] != arole:
							db("update stat set arole=? where jid=?", (arole, source_))
							db.commit()

def init_stat_base(conf):
	filename = chkFile(chat_file(conf, UstatsFile))
	if not os.path.isfile(filename):
		with database(filename) as db:
			db("create table stat (jid text, arole text, joined text, joins integer, seen text, leave text, nicks text)")
			db.commit()
			user_stats_spike(conf, db)
	UstatsDesc[conf] = threading.Semaphore()

def edit_stat_desc(conf):
	del UstatsDesc[conf]

try:
	from itypes import Database as database
	command_handler(command_user_stats, 11, "user_stats")
	command_handler(command_here, 10, "user_stats")

	handler_register("01si", init_stat_base)
	handler_register("04si", edit_stat_desc)
	handler_register("04eh", calc_stat_04eh)
	handler_register("05eh", calc_stat_05eh)
	handler_register("06eh", calc_stat_06eh)
	handler_register("07eh", calc_stat_07eh)
except ImportError:
	Print("#! Warning: can't import itypes.Database. Is sqlite3 module installed?", color2)