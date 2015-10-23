# BS mark.1-55
# /* coding: utf8 */
# BlackSmith Bot Plugin
# Copyright Url Shortener (by service u.to) © simpleApps CodingTeam (Fri Oct 28 18:54:26 2011)
# This program published under Apache 2.0 license
# See LICENSE.txt for more details

#-extmanager-extVer:2.2-#
#-extmanager-conflict:extensions/isgd-shortener.py-#

def url_shortener(mType, source, body):
	if body:
		protocol, _ = body.split("://")[:2]
		raw = _.split("/", 1)
		if len(raw) > 1:
			domain, page = raw
			page = "/" + page
		else:
			domain, page = raw[0], ""
		domain = IDNA(domain)
		if not chkUnicode(page, "(~#?!%&+=,:;*|)"):
			page = urllib.quote(str(page))
		_url = u"%s://%s%s" % (protocol, domain, page)
		headers = {"Accept": "application/xml, text/xml */*",
				   "Accept-Language": "ru-ru,ru; q=0.5",
				   "Accept-Encoding": "deflate",
				   "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				   "User-Agent": UserAgents["BlackSmith"]}
		data = urllib.urlencode(dict(a = "add", url = _url))
		request = urllib2.Request("http://u.to/", data, headers)
		resp = urllib2.urlopen(request)
		html = resp.read()
		regExp = re.search("#shurlout'\)\.val\('(.*)'\)\.show\(\)\.focus\(\)", html)
		if regExp:
			answer = regExp.group(1)
		else:
			regErrExp = re.search("<div class=\"myWinLoadSF\">(.*)</div>", html)
			answer = regErrExp.group(1)
	else:
		answer = u"Ошибка."
	reply(mType, source, answer)

command_handler(url_shortener, 11, "uto-shortener")