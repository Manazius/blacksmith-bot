# BS mark.1-55
# /* coding: utf-8 */
# Author: WithcerGeralt
# Ported from BlackSmith m.2 
# (c) simpleApps, 2011


def decodeHTML(data):
	data = stripTags(data)
	data = uHTML(data)
	return data.strip()

def gismeteo(mType, source, body):
	if body:
		ls = body.split()
		Numb = ls.pop(0)
		if ls and Numb.isdigit():
			City = body[(body.find(Numb) + len(Numb) + 1):].strip()
			Numb = int(Numb)
		else:
			Numb, City = (None, body)
		if -1 < Numb < 13 or not Numb:
			try:
				data = read_url("http://m.gismeteo.ru/citysearch/by_name/?" +\
									 urlencode({"gis_search": City.encode("utf-8")}), UserAgents["BlackSmith"])
			except:
				answer = u"Не могу получить доступ к странице."
			else:
				data = data.decode("utf-8")
				data = data = re_search(data, "<a href=\"/weather/", "/(1/)*?\">", "\d+")
				if data:
					if Numb != None:
						data = str.join(chr(47), [data, str(Numb) if Numb != 0 else "weekly"])
					try:
						data = read_url("http://m.gismeteo.ru/weather/%s/" % data, UserAgents["BlackSmith"])
					except:
						answer = u"Не могу получить доступ к странице."
					else:
						data = data.decode("utf-8")
						mark = re_search(data, "<th colspan=\"2\">", "</th>")
						if Numb != 0:
							comp = re.compile('<tr class="tbody">\s+?<th.*?>(.+?)</th>\s+?<td.+?/></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>\s+?</tr>\s+?<tr class="dl">\s+?<td>&nbsp;</td>\s+?<td class="clpersp"><p>(.*?)</p></td>\s+?</tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl"><td class="left">(.+?)</td><td>(.+?)</td></tr>\s+?<tr class="dl bottom"><td class="left">(.+?)</td><td>(.+?)</td></tr>', 16)
							list = comp.findall(data)
							if list:
								ls = [(decodeHTML(mark) if mark else "\->")]
								for data in list:
									ls.append("{0}:\n\t{2}, {1}\n\t{3} {4}\n\t{5} {6}\n\t{7} {8}".format(*data))
								answer = decodeHTML(str.join(chr(10), ls)) + "\n*** Погода предоставлена сайтом GisMeteo.ru"
							else:
								answer = u"Проблемы с разметкой."
						else:
							comp = re.compile('<tr class="tbody">\s+?<td class="date" colspan="3"><a.+?>(.+?)</a></td>\s+?</tr>\s+?<tr>\s+?<td rowspan="2"><a.+?/></a></td>\s+?<td class="clpersp"><p>(.+?)</p></td>\s+?</tr>\s+?<tr>\s+?<td.+?>(.+?)</td>', 16)
							list = comp.findall(data)
							if list:
								ls = [(decodeHTML(mark) if mark else "\->")]
								for data in list:
									ls.append("{0}:\n\t{1}, {2}".format(*data))
								answer = decodeHTML(str.join(chr(10), ls)) + "\n*** Погода предоставлена сайтом GisMeteo.ru"
							else:
								answer = u"Проблемы с разметкой..."
				else:
					answer = u"Ничего не найдено..."
		else:
			answer = "SyntaxError: Invalid Syntax"
	else:
		answer = u"Недостаточно параметров."
	reply(mType, source, answer)

command_handler(gismeteo, 10, "gismeteo")