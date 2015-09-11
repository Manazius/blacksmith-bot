# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
# © WitcherGeralt (WitcherGeralt@jabber.ru)


def command_calendar(mType, source, body):
	import calendar
	date = time.gmtime()
	y, z = 0, 0
	if body:
		body = body.split()
		x = body.pop(0)
		if check_nubmer(x):
			z = int(x)
			if body and check_number(body[0]):
				y = int(body.pop(0))
	if z not in xrange(1, 13):
		y = (date.tm_year)
		z = (date.tm_mon)
	elif y <= 0:
		y = (date.tm_year)
	Ans_1 = "\nCalendar:\n*\n*\tM/Y: %s\n*\n*\t%s\n*\nCurrent Date/Time: %s"
	clndr = ((calendar.month(y, z)).strip()).splitlines()
	Ans_2 = clndr.pop(0)
	Ans_3 = "\n*\t".join(clndr)
	reply(mType, source, Ans_1 % (Ans_2, Ans_3, time.asctime(date)))
	del calendar

command_handler(command_calendar, 10, "calend")