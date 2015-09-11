# BS mark.1-55
# /* coding: utf-8 */

# Idea © WitcherGeralt, 2010 — 2011.
# (c) simpleApps, 2011 — 2013.


ALARM_FILE = 'dynamic/alarm.txt'
ALARM_LIST = {}

def alarmConfig(mType, source, body):
	jid = handler_jid(source[0])
	answer = ""
	if body:
		if len(body) <= 256:
			args = body.split(None, 1)
			if args[0] == "+":
				data = args[1]
				if jid not in ALARM_LIST:
					ALARM_LIST[jid] = list()

				if jid not in ADLIST and len(ALARM_LIST[jid]) > 5:
					return reply(mType, source, u"Лимит напомниналок исчерпан!")
					
				if data not in ALARM_LIST:
					ALARM_LIST[jid].append(data)
					answer = u"Добавил под номером %i." % len(ALARM_LIST[jid])
				else:
					answer = u"Такая напоминалка уже есть. Номер: %i." % ALARM_LIST[jid].index(data)

			elif args[0] == "-":
				if args[1].isdigit() and len(ALARM_LIST.get(jid, "")) > (int(args[1]) - 1) and int(args[1]) > 0:
					ALARM_LIST[jid].remove(ALARM_LIST[jid][int(args[1]) - 1])
					answer = u"Удалил запись под номером %s." % args[1]
				else:
					answer = u"Либо «%s» не число, либо нет записи с таким номером." % args[1]
			
			elif args[0] == u"очистить":
				if jid in ALARM_LIST:
					del ALARM_LIST[jid]
					answer = u"Очищено."
				else:
					answer = u"Пусто."

 			elif args[0].isdigit():
				_id = int(args[0]) - 1
				_alarm = ALARM_LIST[jid]
				if len(_alarm) > _id > -1:
					answer = u"\n%d. %s" % (_id + 1, _alarm[_id])
				else:
					answer = "Пункт #%d не найден!" % (_id +1)
	else:
		answer = "\n"
		if ALARM_LIST.get(jid):
			for x, y in enumerate(ALARM_LIST[jid], 1):
				answer +=  u"%i. %s.\n" % (x, y)
		else:
			answer = u"На тебя нет ничего."
	write_file(ALARM_FILE, str(ALARM_LIST))
	reply(mType, source, answer)

def alarmWork(chat, nick, afl, role, status, text):
	jid = handler_jid("%s/%s" % (chat, nick))
	answer = "\nНапоминаю:\n"
	if ALARM_LIST.get(jid):
		for x, y in enumerate(ALARM_LIST[jid], 1):
			answer +=  u"%i. %s.\n" % (x, y)
		msg(chat + "/" + nick, answer)

def alarmInit():
	if initialize_file(ALARM_FILE):
		globals()["ALARM_LIST"] = eval(read_file(ALARM_FILE))
	else:
		Print('\n\nError: can`t create alarm.txt!', color2)

handler_register("04eh", alarmWork)
command_handler(alarmConfig, 10, "alarm")
handler_register("00si", alarmInit)