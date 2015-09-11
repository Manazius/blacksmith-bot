# BS mark.1-55
# /* coding: utf-8 */

# BlackSmith Extension Manager
# This plugin distributed under Apache 2.0 license.
# (c) simpleApps, 2012 — 2013.

## NOTICE: 
##			All plugins that depend from another plugins or files (not help files that placed in help dir)
##			Must be contain this code: #-extmanager-depends:depend1;depend2;depend3-#
##			Where depend1, depend2 and depend3 are depends of this plugin.
##			Read plugins comments (from /proposed) for know more.
import urllib

svnUrl = "http://blacksmith-bot.googlecode.com/svn/proposed/%s/"
extFile = "dynamic/extensions.txt"

def urlsplit(url):
	if url and url.count("/"):
		strippedUrl = url.rstrip("/")
		tailIndex = strippedUrl.rfind("/")
		head = strippedUrl[:tailIndex]
		tail = strippedUrl[tailIndex:]
		url = (head, tail)
	return url
	
def getSize(url):
	request = urllib.urlopen(url)
	return int(request.headers.get("Content-Length"))
	
def getDepsSize(depList):
	size = int()
	for dep in depList:
		size += getSize(svnUrl % dep)
	return size
	
def saveDeps(path):
	Dir = os.path.split(path)[0]	
	if Dir and not os.path.exists(Dir):
		os.makedirs(Dir)
	return path
	
def getDeps(depList = [], plugin = None):
	if plugin:
		depList = findDeps(read_url(svnUrl % "extensions/%s" % plugin))
	if depList:
		for dep in depList:
			if dep.endswith(".dir"):
				Dir = dep[:-4]
				if not os.path.exists(Dir):
					os.makedirs(Dir)
			else:
				urllib.urlretrieve(svnUrl % dep, saveDeps(dep)) 

def findDeps(data, join = None):
	match = re.search("#-extmanager-depends:(.*)-#", data)
	if match:
		dep = match.group(1)
		depList = dep.split(";")
		if join:
			return str.join(join, depList)
		return depList

def findExtVer(data):
	match = re.search("#-extmanager-extVer:(.*)-#", data)
	if match:
		ver = match.group(1)
		return ver
	return "1.0"

def findConflicts(data):
	match = re.search("#-extmanager-conflict:(.*)-#", data)
	if match:
		rawConflicts = match.group(1)
		if ";" in rawConflicts:
			return rawConflicts.split(";")
		return [rawConflicts]

def extManager(mType, source, args):
	if args:
		answer = str()
		a = args.split(None, 1)
		name, fullName = a[0], a[0] + ".py"
		afterA0 = args[-1]
		extList = re.findall("\">(.*\.py)</a></li>", read_url(svnUrl % "extensions")) #"
		extList = [x[:-3] for x in extList]

		if a[0] == u"лист":
			answer = u"\nВсего доступно %d плагинов:\n" % len(extList)
			answer = enumerated_list(extList)
			answer = answer.rstrip("\n;") + "."

		elif a[0] in extList and len(a) > 1:
			if a[1] in (u"инфо", "установить"):
				data = read_url(svnUrl % "extensions/%s" % fullName)
				depList = findDeps(data)
				conflicts = findConflicts(data)
				if a[1] == u"инфо":
					pluginInfo = eval(read_url(svnUrl % ("help/" + a[0])).decode("utf-8"))
					commandList = [pluginInfo[x]["cmd"] for x in pluginInfo.keys()]
					if depList:
						jDepList = str.join(", ", depList)
						sizeOf = byteFormat(getDepsSize(depList) + getSize(svnUrl % "extensions/%s" % fullName))
					if conflicts:
						conflictList = str.join(", ", conflicts)
					commandList = str.join(", ", commandList)
					version = findExtVer(data)
					answer =\
						"\nПлагин: %(name)s (версия %(version)s).\nСодержит команды: %(commandList)s."
					if depList:
						answer +=\
							"\nДля плагина требуется: %(jDepList)s, после установки будет занятно примерно %(sizeOf)s."
					if conflicts:
						answer += " Также будут удалены: %(conflictList)s."
					answer = answer % vars()
	
				elif a[1] == u"установить":
					extensions = eval(read_file(extFile))
					urllib.urlretrieve(svnUrl % "extensions/%s" % fullName, "extensions/%s" % fullName)
					urllib.urlretrieve(svnUrl % "help/" + a[0], "help/%s" % a[0])
					getDeps(depList)
					extensions[fullName] = findExtVer(read_url(svnUrl % "extensions/%s" % fullName))
					
					if conflicts:
						for x in conflicts:
								if os.path.isfile(x):
									try:
										os.remove(x)
										conflicts.remove(x)
										del extensions[x] #!
									except (KeyError, OSError):
										pass
								else:
									conflicts.remove(x)
					answer = u"Плагин «%s» успешно установлен"
					try:
						execfile("./extensions/%s" % fullName, globals())
						answer += " и подгружен. Возможно, понадобится перезапуск бота."
					except:
						answer += u", однако подгрузка не удалась: \n%s" % (returnExc())
					answer = answer % name
					if conflicts:
						conflicts = str.join(", ", conflicts)
						answer += u" Также, не удалось устранить следующие конфликты: %(conflicts)s."

			elif a[1] == u"удалить":
				if os.path.exists("./extensions/%s" % fullName):
					size = 0
					extensions = eval(read_file(extFile))
					depList = findDeps(read_file("./extensions/%s" % fullName))
					try:
						for x in ("./extensions/%s" % fullName, "./help/%s" % name):
							size += os.path.getsize(x)
							os.remove(x)
						answer += u"Плагин «%(name)s» успешно удалён."
						if fullName in extensions.keys():
							del extensions[fullName]
							write_file(extFile, str(extensions))
					except:
						answer += u"Удаление плагина «%(name)s» не удалось."
							
					if depList:
						for dep in depList:
							if os.path.exists(dep):
								size += os.path.getsize(dep)
								if not os.path.isdir(dep):
									os.remove(dep)
						depList = str.join(", ", depList)
						answer += u"\nТакже были удалены: %(depList)s."
					size = byteFormat(size)
					answer += "\nОсвобождённое дисковое пространство: %(size)s."
				else:
					answer = u"Плагин «%(name)s» не найден!"
			else:
				answer = u"Ошибка. Возможно, этого плагина нет в списке или вы указали несуществующий параметр."

		elif a[0] == u"upgrade":
			answer = u"Обновлять нечего."
			extensions = eval(read_file(extFile))
			toUpdate = dict()
			fail, ok = [], []
			for ext in extensions.keys():
				localVer = extensions[ext]
				try:
					remoteVer = findExtVer(read_url(svnUrl % "extensions/%s" % ext))
				except Exception:
					remoteVer = localVer
					fail.append(ext)

				if localVer != remoteVer:
					toUpdate[ext] = remoteVer
			if toUpdate:
				answer = "\nОбновлено %d плагинов: "
				jDepList = []
				for ext in toUpdate.keys():
					name = ext[:-3]
					depList = findDeps(read_url(svnUrl % "extensions/%s" % ext))
					if depList:
						jDepList.extend(depList)
					urllib.urlretrieve(svnUrl % "extensions/%s" % ext, "extensions/%s" % ext)
					urllib.urlretrieve(svnUrl % "help/" + name, "help/%s" % name)
					getDeps(depList)
					extensions[ext] = toUpdate[ext]
					try:
						execfile("extensions/%s" % ext, globals())
						ok.append(ext)
					except:
						fail.append(ext)

				answer = answer % len(ok) + str.join(", ", ok) + "."
				if jDepList:
					jDepList = str.join(", ", jDepList)
					answer += "\nТакже были установлены следующие зависимости: %(jDepList)s."
				if fail:
					answer += "\n• Не удалось найти или подгрузить следующие плагины: %s." % (str.join(", ", fail))
				answer = answer % vars()
				write_file(extFile, str(extensions))
			
		reply(mType, source, answer % vars())

def extmanager_init():
	if not initialize_file(extFile, "{}"):
		delivery(u"Внимание! Не удалось создать extmanager.txt!")

command_handler(extManager, 100, "extmanager")

handler_register("02si", extmanager_init)