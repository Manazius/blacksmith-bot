# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  distance.py
#  © simpleApps, 2013.

distance_url = "http://lardi-trans.com/distance/print/?action=submited&town1=%(town0)s&town2=%(town1)s&marh_type=2&reserv=on&country_out=on"

def command_distance(mType, source, body):
	if body:
		args = body.split()
		if len(args) == 2:
			town0, town1 = (urllib.quote(str(x)) for x in args)
			data = read_link(distance_url % vars())
			if not "<span class=\"fontTitle\">" in data:
				try:
					answer = stripTags(uHTML(re_search(data, "<strong>", "<table>")))
				except:
					answer = u"Что-то не так..."
			else:
				answer = u"Видимо, такого города и нет в природе..."
			reply(mType, source, answer)

		

command_handler(command_distance, 11, "distance")
