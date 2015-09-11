# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  status_plugin.py

#  Initial Copyright © 2007 Als <Als@exploit.in>

USER_STATUS = {}

def handler_status(type, source, nick):
	if source[1] in GROUPCHATS:
		if nick:
			if nick in USER_STATUS[source[1]]:
				status = USER_STATUS[source[1]][nick]['status']
				stmsg = USER_STATUS[source[1]][nick]['stmsg']
				if stmsg:
					repl = status+' ('+stmsg+')'
				else:
					repl = status
			else:
				repl = u'хрен его знает'
		else:
			status = USER_STATUS[source[1]][source[2]]['status']
			stmsg = USER_STATUS[source[1]][source[2]]['stmsg']
			if stmsg:
				repl = status+' ('+stmsg+')'
			else:
				repl = status
		reply(type, source, repl)
	else:
		reply(type, source, u'я не умею читать ростер-статус')

def status_change(Prs):
	instance = Prs.getFrom()
	conf = instance.getStripped()
	nick = instance.getResource()
	if conf not in USER_STATUS:
		USER_STATUS[conf] = {}
	status = Prs.getShow()
	if not status:
		status = 'online'
	stmsg = Prs.getStatus()
	if not stmsg:
		stmsg = ''
	USER_STATUS[conf][nick] = {'status': status, 'stmsg': stmsg}

handler_register("02eh", status_change)
command_handler(handler_status, 10, "status")
