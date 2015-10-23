# BS mark.1-55
# /* coding: utf8 */
# BlackSmith Bot Plugin
# Copyright Url Shortener (by service u.to) © simpleApps CodingTeam (Fri Oct 28 18:54:26 2011)
# This program published under Apache 2.0 license
# See LICENSE.txt for more details

#-extmanager-extVer:1.0-#
#-extmanager-conflict:extensions/uto-shortener.py-#

def isGd_shortener(mType, source, body):
	if body:
		data = urllib.urlencode(dict(format = "json", url = body))
		data = read_url("http://is.gd/create.php?%s" % data, UserAgents["BlackSmith"])
		data = simplejson.loads(data)
		answer = data["shorturl"]
	else:
		answer = u"Ошибка."
	reply(mType, source, answer)

command_handler(isGd_shortener, 11, "isgd-shortener")