# BS mark.1-55
# /* coding: utf-8 */

# © simpleApps, 21.05.2012 (12:38:47)
# Web site header detector

# RC-5!
#-extmanager-extVer:2.9.4-#

import re
import zlib
import urllib2

comp_link = re.compile("(https?)://([^\s'\"<>/]+)([^\s'\"<>]+)")
comp_charset = re.compile("(.+);[ ]?charset=(.+)")
comp_charset_alt = re.compile("charset=['\"]?(.+?)[\s'\"/>]+?")

urlDetect = {"list": [], "last": None, 
			 "urlAllowedChars": "([~#?!%&+=,:;*]|)",
			 "unAllowedChars": [unichr(x) for x in xrange(32) if x not in (9, 10, 13)]}

urlDetect["unAllowedChars"].append(unichr(57003))
urlDetect["unAllowedChars"].append(unichr(65535))

def contentTypeParser(opener, data):
	Charset, Type = None, opener.headers.get("Content-Type")
	try:
		if Type and Type.count(";"):
			found = comp_charset.search(Type)
			if found:
				Type, Charset = found.groups()
				Charset = Charset.strip("'\"").lower()
				if Charset == "unicode":
					Charset = "utf-8"
				if Charset.count("."):
					Charset = Charset.split(".")[1]
		elif (not Charset and Type == "text/html") or opener.url.endswith((".html", ".htm")):
			Charset = comp_charset_alt.search(data)
			if Charset:
				Charset = Charset.group(1)
	except Exception:
		lytic_crashlog(contentTypeParser, "", u"During the search encoding on %s." % opener.url)
	if not Charset:
		Charset = "utf-8"
	return (Type, Charset) 

def urlParser(body, TitleMSG = u"%s", callType = "auto"):
	data = comp_link.search(body)
	answer = ""
	if data:
		try:
			protocol, domain, page = data.groups()
			domain = IDNA(domain)
			page = page.strip("'.,\\]\"")
			if not chkUnicode(page, urlDetect["urlAllowedChars"]):
				page = urllib.quote(str(page))
			url = u"%s://%s%s" % (protocol, domain, page)
			if url == urlDetect["last"] and callType == "auto":
				return None
			urlDetect["last"] = url
			req = urllib2.Request(url)
			req.add_header("User-agent", UserAgents["BlackSmith"])
			opener = urllib2.urlopen(req)
			headers  = opener.headers
			cType = headers.get("Content-Type", "")
			if ("text/html" in cType) or ("application/xhtml+xml" in cType) or url.endswith((".html", ".htm")):
				if headers.get("Content-Encoding") == "gzip":
					data = opener.read()
					data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
				else:
					data = opener.read(7000)
				Type, Charset = contentTypeParser(opener, data)
				title = getTagData("title", data)
				title = title.decode(Charset)
				if title:
					answer = TitleMSG % uHTML(title).replace("\n", "").replace("\r","").strip()
			else:
				fullUrl = opener.url
				name = fullUrl.split("/")[-1]
				Type = headers.get("Content-Type", "")
				Size = int(headers.get("Content-Length", 0))
				Date = headers.get("Last-Modified") or headers.get("Date") or ""
				try:
					Date = time.strptime(Date, "%a, %d %b %Y %H:%M:%S GMT")
					Date = time.strftime("%d.%m.%Y %H:%M:%S GMT", Date)
				except ValueError: 
					pass
				answer += "Файл: " + name
 				if Size:
 					answer += u" — " + byteFormat(Size)
 				if Type:
 					answer += u" • " + Type.split()[0].strip(",;.")
 				if Date: 
 					answer += u"\nПоследнее изменение: %s." % Date
			if answer:
				answer = replace_all(answer, urlDetect["unAllowedChars"], "")
		except (urllib2.HTTPError, urllib2.URLError, urllib2.socket.error) as e:
			answer = "%s: %s" % (e.__class__.__name__, e.message or str(e))
		except: 
			lytic_crashlog(urlWatcher, "", "While parsing \"%s\"." % locals().get("url", body))
	return answer.decode("utf-8")

def urlWatcher(raw, mType, source, body):
	if mType == "public" and (source[1] in urlDetect["list"]) and has_access(source[0], 11, source[1]):
		if len(body) < 500:
			answer = urlParser(body, u"Заголовок: %s")
			if answer:
				msg(source[1], answer)

			
def urlWatcherConfig(mType, source, args):
	answer = "Что?"
	if args:	
		args = args.strip()[:500]
		argv = args.split()
		answer = ""
		if args in ("1", "0"):
			if has_access(source[0], 20, source[1]):
				if args == "1":
					if source[1] in urlDetect["list"]:
						answer = u"Уже включено."
					else:
						urlDetect["list"].append(source[1])
						write_file("dynamic/urlWatcher.txt", str(urlDetect["list"]))
						answer = u"Включил автодетект ссылок."
				elif args == "0":
					if source[1] in urlDetect["list"]:
						urlDetect["list"].remove(source[1])
						write_file("dynamic/urlWatcher.txt", str(urlDetect["list"]))
						answer = u"Выключил автодетек ссылок."
					else:
						 answer = u"Не включено."
				else:
					answer = u"Неизвестный параметр."
			else:
				answer = "Недостаточный доступ."
		else:
			argv = argv[:10]
			for link in argv:
				answer += "\n%s ­— %s" % (link, urlParser(link, callType = "manual"))
	reply(mType, source, answer)

def urlWatcherConfig_load():
	if initialize_file("dynamic/urlWatcher.txt", "[]"):
		urlDetect["list"] = eval(read_file("dynamic/urlWatcher.txt"))

def urlWatcher_04si(chat):
	if chat in urlDetect:
		urlDetect["list"].remove(chat)
		write_file("dynamic/urlWatcher.txt", str(urlDetect["list"]))

handler_register("01eh", urlWatcher)

command_handler(urlWatcherConfig, 11, "urldetect")

handler_register("00si", urlWatcherConfig_load)
handler_register("04si", urlWatcher_04si)