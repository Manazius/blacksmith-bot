# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  new_year_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

def handler_new_year(type, source, body):
	list = [u"До нового года (по GMT) осталось:"]
	Time = time.gmtime()
	t0 = (365 if (Time.tm_year%4) else 366)
	t1 = (t0 - Time.tm_yday)
	t2 = (23 - Time.tm_hour)
	t3 = (59 - Time.tm_min)
	t4 = (59 - Time.tm_sec)
	if t1:
		list.append("%d Дн." % (t1))
	if t2:
		list.append("%d Час." % (t2))
	if t3:
		list.append("%d Мин." % (t3))
	if t4:
		list.append("%d Сек." % (t4))
	if len(list) == 1:
		list = [u"С новым годом!"]
	reply(type, source, " ".join(list))

command_handler(handler_new_year, 10, "new_year")
