#! /usr/bin/env python
# /* coding: utf-8 */

#  BlackSmith Bot Core
#  BlackSmith.py

#  Thanks to:
#    Als [Als@exploit.in]
#    Evgen [meb81@mail.ru]
#    dimichxp [dimichxp@gmail.com]
#    Boris Kotov [admin@avoozl.ru]
#    Mike Mintz [mikemintz@gmail.com]

#  This program distributed under Apache 2.0 license.
#  See license.txt for more details.
#  © WitcherGeralt, based on Talisman by Als (Neutron by Gh0st)
#  The new bot life © simpleApps 2011 — 2013.

## Imports.
from traceback import format_exc, print_exc
import gc, os, re, sys, time, random, threading

## Local dir.
core = getattr(sys.modules["__main__"], "__file__", None)
if core:
	core = os.path.abspath(core)
	root = os.path.dirname(core)
	if root:
		os.chdir(root)

sys.path.insert(0, "library.zip")

from enconf import *
import xmpp, macros
import json as simplejson

## Stats.
INFO = {"start": 0, "msg": 0, "prs": 0, "iq": 0, "outmsg": 0, "outiq": 0,
		"cmd": 0, "thr": 0, "fr": 0, "fw": 0, "fcr": 0, "cfw": 0, "errs": 0, "zc": 0}
RSTR = {"AUTH": [], "BAN": [], "VN": "off"}
LAST = {"time": 0, "cmd": "start", "error": None}

## Colored stdout.
color0 	= xmpp.debug.color_none
color1 	= xmpp.debug.color_brown
color2 	= xmpp.debug.color_bright_red
color3 	= xmpp.debug.color_green
color4 	= xmpp.debug.color_bright_blue
colored = xmpp.debug.colors_enabled

def exec_(instance, args = ()):
	try:
		code = instance(*args)
	except Exception:
		code = None
	return code

def text_color(text, color):
	if colored and color:
		text = color+text+color0
	return text

def Print(text, color = False):
	try:
		print text_color(text, color)
	except:
		pass

## Increase convenience.
def try_sleep(slp):
	try:
		time.sleep(slp)
	except KeyboardInterrupt:
		os._exit(0)

def Exit(text, exit, slp):
	Print(text, color2); try_sleep(slp)
	if exit:
		os._exit(0)
	else:
		os.execl(sys.executable, sys.executable, os.path.abspath(sys.argv[0]))

## Configuration.
GENERAL_CONFIG_FILE = 'static/source.py'
GLOBACCESS_FILE = 'dynamic/access.txt'
GROUPCHATS_FILE = 'dynamic/chats.txt'
QUESTIONS_FILE = 'static/veron.txt'
ROSTER_FILE = 'dynamic/roster.txt'
EXT_DIR = 'extensions'
PID_FILE = 'PID.txt'

BOT_OS, BOT_PID = os.name, os.getpid()

def PASS_GENERATOR(codename, Number):
	symbols = "".join(ascii_tab)
	for Numb in xrange(Number):
		codename += random.choice(symbols)
	return codename

if os.path.exists(GENERAL_CONFIG_FILE):
	try:
		execfile(GENERAL_CONFIG_FILE)
		BOSS_PASS = (PASS_GENERATOR("", eval(BOSS_PASS[7:])) if "/random" in BOSS_PASS else BOSS_PASS)
		reload(sys).setdefaultencoding("utf-8")
		execfile("static/versions.py")
	except Exception, e:
		Exit(str(e), 1, 12)
else:
	Exit("\n#! General config file not found! Exiting.", 1, 5)

if BOT_OS == "nt":
	os.system("Title BlackSmith - %s" % (Caps))

## Lists of handlers.
Handlers = { "01eh": [], "02eh": [],
			 "03eh": [], "04eh": [],
			 "05eh": [], "06eh": [],
			 "07eh": [], "08eh": [],
			 "09eh": [], "00si": [], 
			 "01si": [], "02si": [], 
			 "03si": [], "04si": [] }

## FOR eXample:
# *si = *stage-init
# 01eh = message
# 02eh = presence
# 03eh = IQ
# 04eh = user join
# 05eh = user leave
# 06eh = user nick change
# 07eh = user role change
# 08eh = user status change
# 09eh = topic recieved

## Dictionaries, lists.
MORE = {}
Flood = []
ADLIST = []
ANSWER = {}
PREFIX = {}
STATUS = {}
ERRORS = {}
COMMOFF = {}
COMMSTAT = {}
COMMANDS = {}
RUNTIMES = {}
BOT_NICKS = {}
QUESTIONS = {}
ACCBYCONF = {}
CONFACCESS = {}
GLOBACCESS = {}
GROUPCHATS = {}
UNAVAILABLE = []
COMMAND_HANDLERS = {}
cPrefs = ("!", "@", "#", ".", "*", "?", "`")


XEPs = set((xmpp.NS_VERSION, 
			xmpp.NS_PING, 
			xmpp.NS_TIME, 
			xmpp.NS_URN_TIME,
			xmpp.NS_LAST, 
			xmpp.NS_DISCO_INFO,
			xmpp.NS_CAPS,
			xmpp.NS_SASL,
			xmpp.NS_TLS,
			xmpp.NS_MUC,
			xmpp.NS_ROSTER,
			xmpp.NS_RECEIPTS))

MACROS = macros.Macros()

Sequence = threading.Semaphore()

from sTools import *
## os info.
os_simple = ""
if os.name == "nt":
	from platform import win32_ver
	os_name = " ".join([ntDetect(), win32_ver()[0], win32_ver()[2]])
	os_simple = os_name
	del win32_ver

elif os.name == "posix":
	from platform import dist
	dist, uname = dist(), os.uname()
	if dist[0]:
		os_simple = u"%s, %s" % (dist[0], uname[0])
		os_name = "POSIX (%s %s)" % (os_simple, uname[2])
	else:
		os_simple = uname[0]
		os_name = "POSIX (%s, %s)" % (os_simple, uname[2])
	del dist, uname
else:
	os_name = os.name.upper()

os_name = os_name.strip() + " " + getArchitecture()

from webtools import *
UserAgents["BlackSmith"] = "Mozilla/5.0 (%s; %d.%d; ru) BlackSmith XMPP-BOT mark.1" % (os_simple, BOT_VER, CORE_MODE)
del ntDetect, getArchitecture, os_simple

## File workers.
def check_file(chat = None, file = None, data = "{}"):
	if chat:
		filename = chkFile('dynamic/%s/%s' % (chat, file))
	else:
		filename = 'dynamic/%s' % (file)
	return initialize_file(filename, data)

def initialize_file(name, data = "{}"):
	name = chkFile(name)
	if len(name.split('/')) >= 5:
		return False
	if os.path.exists(name):
		return True
	try:
		folder = os.path.dirname(name)
		if folder and not os.path.exists(folder):
			os.makedirs(folder, 0755)
		with open(name, "w") as fp:
			INFO['fcr'] += 1
			fp.write(data)
	except:
		lytic_crashlog(initialize_file)
		return False
	return True

def read_file(name):
	with open(chkFile(name), "r") as fp:
		INFO['fr'] += 1
		return fp.read()

def write_file(name, data, mode = "w"):
	with Sequence:
		with open(chkFile(name), mode) as fp:
			INFO['fw'] += 1
			fp.write(data)

iAmConnected = lambda: "jClient" in globals() and jClient.isConnected()

## Crashfile writer.
def lytic_crashlog(handler, command = None, comment = None):
	dir, handler, number, trace = "feillog", handler.func_name, (len(ERRORS.keys()) + 1), format_exc()
	text = str()
	if trace != LAST["error"]:
		LAST["error"] = trace
		if iAmConnected():
			if command:
				error = u"команды «%s» (%s)" % (command, handler)
			else:
				error = u"процесса «%s»" % handler
			text += u"При выполнении %s произошла ошибка!" % error
		else:
			Print("\n\nError: can't execute \"%s\"!" % handler, color2)
		INFO['cfw'] += 1
		filename = "%s/error[%d]%s.crash" % (dir, INFO["cfw"], time.strftime("[%H.%M.%S][%d.%m.%Y]"))
		ERRORS[number] = filename
		if not os.path.exists(dir):
			os.mkdir(dir, 0755)
		if comment:
			trace += u"\nDeveloper's Comment: %s" % comment
		write_file(filename, trace)
		if iAmConnected():
			if BOT_OS == "posix":
				Text = u"%(text)s Ошибку смотри по командам: \"ошибка %(number)d\" или \"sh cat %(filename)s\""
			else:
				Text = u"%(text)s Ошибку смотри по команде: \"ошибка %(number)d\" (крэшфайл — %(filename)s)" 
			delivery(Text % vars())
		else:
			Print("\n\n#-# Error #%d, name: %s" % (number, filename), color2)

## Handlers register.
def handler_register(ls, handler):
	name = handler.func_name
	for instance in Handlers[ls]:
		if name == instance.func_name:
			Handlers[ls].remove(instance)
	Handlers[ls].append(handler)

## Command handler.
def command_handler(instance, access = 0, plug = "default"):
	try:
		command = eval(read_file("help/%s" % plug).decode('utf-8'))[instance.func_name]["cmd"]
	except:
		print_exc()
		command = instance.func_name.lower()
		Print("\nPlugin \"%s\" has no help and command name. New command name: %s." % (plug, command), color2)
	if COMMANDS.get(command) or COMMAND_HANDLERS.get(command):
		if plug != COMMANDS[command].get("plug"):
			Print("\nCommands in \"%s\" and \"%s\" are repeated." % (plug, COMMANDS[command].get("plug")), color2)
			command += "1"
	if command not in COMMSTAT:
		COMMSTAT[command] = {'col': 0, 'users': []}
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'plug': plug, 'access': access}

## Call, execute handlers.
def execute_handler(handler_instance, list = (), command = None):
	try:
		handler_instance(*list)
	except (SystemExit, KeyboardInterrupt):
		pass
	except Exception:
		lytic_crashlog(handler_instance, command)

def call_sfunctions(ls, list = ()):
	for handler in Handlers[ls]:
		execute_handler(handler, list)

def composeTimer(timeout, handler, Name = None, list = (), command = None):
	INFO['thr'] += 1
	if not Name:
		Name = "Timer-%d" % (INFO['thr'])
	Timer_ = threading.Timer(timeout, execute_handler, (handler, list, command,))
	Timer_.name = Name
	return Timer_

def composeThr(handler, Name, list = (), command = None):
	INFO['thr'] += 1
	Name = "%s-%d" % (Name, INFO['thr'])
	return threading.Thread(None, execute_handler, Name, (handler, list, command,))

def StartThr(Thr, Number = 0):
	if Number > 2:
		raise RuntimeError("exit")
	try:
		Thr.start()
	except threading.ThreadError:
		StartThr(Thr, (Number + 1))
	except:
		lytic_crashlog(Thr.start)

def sThread_Run(Thr, handler, command = None):
	try:
		Thr.start()
	except threading.ThreadError:
		try:
			StartThr(Thr)
		except RuntimeError:
			try:
				Thr.run()
			except KeyboardInterrupt:
				raise KeyboardInterrupt("Interrupt (Ctrl+C)")
			except:
				lytic_crashlog(handler, command)
	except:
		lytic_crashlog(sThread_Run, command)

def sThread(name, handler, list = (), command = None):
	sThread_Run(composeThr(handler, name, list, command), handler, command)

def call_efunctions(ls, list = ()):
	for handler in Handlers[ls]:
		sThread(ls, handler, list)

ThrNames = lambda: [Thr._Thread__name for Thr in threading.enumerate()]

def call_command_handlers(command, typ, source, body, callee):
	rAccess = MACROS.get_access(callee, source[1])
	if rAccess < 1:
		rAccess = COMMANDS[command]['access']
	if COMMAND_HANDLERS.has_key(command):
		if has_access(source[0], rAccess, source[1]):
			sThread("command", COMMAND_HANDLERS[command], (typ, source, body), command)
			COMMSTAT[command]["col"] += 1
			jid = handler_jid(source[0])
			if jid not in COMMSTAT[command]['users']:
				COMMSTAT[command]['users'].append(jid)
		else:
			reply(typ, source, u"Недостаточный доступ.")

## Plugins loader.
def load_plugins():
	Print('\n\nLoading extensions:', color4)
	Ok, Feil = [], []
	for ext in sorted(os.listdir(EXT_DIR)):
		if ext.endswith(".py"):
			path = os.path.join(EXT_DIR, ext)
			try:
				data = open(path).read(20)
			except:
				data = str()
			ext_name = ext.split(".")[0]
			if "# BS mark.1-55" in data: # mark-api_version
				try:
					execfile(path, globals()); Ok.append(ext_name)
				except:
					print_exc()
					Feil.append(ext_name)
			else:
				Feil.append(ext_name)
	if Ok:
		Print('\n\nLoaded %d BlackSmith extensions:\n%s' % (len(Ok), ', '.join(sorted(Ok))), color3)
	if Feil:
		Print('\n\nThere are %d unloadable extensions:\n%s' % (len(Feil), ', '.join(sorted(Feil))), color2)
	else:
		Print('\n\nThere are not unloadable extensions!', color3)

## Other.
def load_roster_config():
	if initialize_file(ROSTER_FILE, str(RSTR)):
		globals()['RSTR'] = eval(read_file(ROSTER_FILE))
	else:
		Print('\n\nError: roster config file is not exist!', color2)

def load_quests():
	if os.path.exists(QUESTIONS_FILE):
		globals()['QUESTIONS'] = eval(read_file(QUESTIONS_FILE))
	else:
		Print('\n\nError: questions file is not exist!', color2)

def join_chats():
	if initialize_file(GROUPCHATS_FILE):
		try:
			CONFS = eval(read_file(GROUPCHATS_FILE))
		except KeyboardInterrupt:
			raise KeyboardInterrupt("Interrupt (Ctrl+C)")
		except:
			CONFS = {}
			lytic_crashlog(read_file)
			Print("\nChatrooms file corrupted! Load failed.", color2)
		if CONFS:
			Print('\n\nThere are %d rooms in list:' % len(CONFS.keys()), color4)
			for conf in CONFS.keys():
				BOT_NICKS[conf] = CONFS[conf]['nick']
				join_groupchat(conf, handler_botnick(conf), CONFS[conf]['code'])
	else:
		Print('\n\nError: unable to create chatrooms list file!', color2)

def read_pipe(command):
	try:
		if BOT_OS == "posix":
			pipe = os.popen(command.encode("utf8"))
			out = pipe.read()
		elif BOT_OS == "nt":
			pipe = os.popen("%s" % command.encode("cp1251"))
			out = pipe.read().decode("cp866")
		pipe.close()
	except:
		out = returnExc()
	return out

def returnExc():
	exc = sys.exc_info()
	if any(exc):
		error = "\n%s: %s " % (exc[0].__name__, exc[1])
	else:
		error = `None`
	return error

def handler_botnick(chat):
	if chat in BOT_NICKS:
		return BOT_NICKS[chat]
	return DEFAULT_NICK

def handler_jid(instance, Type = "jid"):
	instance = unicode(instance)
	List = instance.split('/', 1)
	chat = List[0].lower()
	if (len(List) == 2) and GROUPCHATS.has_key(chat):
		if GROUPCHATS[chat].has_key(List[1]):
			return GROUPCHATS[chat][List[1]][Type]
	return chat

def save_conflist(conf, nick = None, code = None):
	if initialize_file(GROUPCHATS_FILE):
		try:
			list = eval(read_file(GROUPCHATS_FILE))
		except:
			list = {}
		if conf not in list:
			list[conf] = {'nick': nick, 'code': code}
		elif nick and conf and code:
			list[conf] = {'nick': nick, 'code': code}
		elif nick and conf:
			list[conf]['nick'] = nick
		elif code and conf:
			list[conf]['code'] = code
		elif conf:
			del list[conf]
		write_file(GROUPCHATS_FILE, str(list))
	else:
		Print("\n\nError: can't append conference into chatrooms list file!", color2)

def memory_usage():
	memory = '0'
	if BOT_OS == 'posix':
		lines = read_pipe('ps -o rss -p %d' % BOT_PID).splitlines()
		if len(lines) >= 2:
			memory = lines[1].strip()
	elif BOT_OS == 'nt':
		lines = read_pipe('TASKLIST /FI "PID eq %d"' % BOT_PID).splitlines()
		if len(lines) >= 3:
			list = lines[3].split()
			if len(list) >= 6:
				memory = (list[4] + list[5])
	return (0 if not check_number(memory) else int(memory))

def command_Prefix(conf, command):
	if command in (u'хелп', u'комлист', u'команды', u'префикс', u'тест'):
		return command
	if PREFIX[conf] == command[:1]:
		return command[1:]
	return 'none_command'

def Prefix_state(combody, bot_nick):
	cmd_nick = combody.split()[0]
	for symbol in (':', ',', '>'):
		cmd_nick = cmd_nick.replace(symbol, '')
	if cmd_nick != bot_nick:
		return False
	return True

enumerated_list = lambda ls: str.join(chr(10), ["%d. %s;" % (numb, line) for numb, line in enumerate(ls, 1)])
check_number = lambda obj: (not exec_(int, (obj,)) is None)

def replace_all(retxt, list, data = False):
	for x in list:
		retxt = retxt.replace(x, data if data != False else list[x])
	return retxt

that_day = lambda: int(time.strftime('%Y%m%d', time.gmtime()))

def formatWord(Numb, ls):
	ls = "{2}/{0}/{1}/{1}/{1}/{2}/{2}/{2}/{2}/{2}/{2}/{2}/{2}/{2}/{2}".format(*ls)
	ls = ls.split(chr(47))
	if Numb in xrange(15):
		edge = ls[Numb]
	else:
		edge = ls[int(str(Numb)[-1])]
	return edge

def timeElapsed(Time):
	ext, ls = [], [("Year", None), 
				   ("Month", 12),  ("Day", 30.4375), 
				   ("Hour", 24), ("Minute", 60), ("Second", 60)]
	while ls:
		lr = ls.pop()
		if lr[1]:
			(Time, Rest) = divmod(Time, lr[1])
		else:
			Rest = Time
		if Rest >= 1.0:
			ext.insert(0, "%d %s%s" % (Rest, lr[0], ("s" if Rest > 1 else "")))
		if not (ls and Time):
			return str.join(chr(32), ext)

def ClearMemory():
	while True:
		sys.exc_clear()
		gc.collect()
		time.sleep(60)
		if MEMORY_LIMIT and memory_usage() > MEMORY_LIMIT:
			sys_exit('memory leak')

## Access handlers.
def load_access_levels():
	if initialize_file(GLOBACCESS_FILE):
		globals()['GLOBACCESS'] = eval(read_file(GLOBACCESS_FILE))
	else:
		Print('\n\nError: access file is not exist!', color2)

def form_admins_list():
	if BOSS not in GLOBACCESS:
		GLOBACCESS[BOSS] = 100
	for jid in GLOBACCESS:
		if GLOBACCESS[jid] > 79:
			ADLIST.append(jid)

def change_local_access(conf, jid, level = 0):
	if conf not in ACCBYCONF:
		ACCBYCONF[conf] = {}
	if level:
		ACCBYCONF[conf][jid] = level
	else:
		ACCBYCONF[conf][jid] = 0

def change_global_access(jid, level = 0):
	if level:
		GLOBACCESS[jid] = level
	else:
		del GLOBACCESS[jid]
	write_file(GLOBACCESS_FILE, str(GLOBACCESS))

def user_level(source, conf):
	jid, level = handler_jid(source), 10
	if GLOBACCESS.has_key(jid):
		level = GLOBACCESS[jid]
	elif CONFACCESS.has_key(conf) and CONFACCESS[conf].has_key(jid):
		level = CONFACCESS[conf][jid]
	elif ACCBYCONF.has_key(conf) and ACCBYCONF[conf].has_key(jid):
		level = ACCBYCONF[conf][jid]
	return level

has_access = lambda source, level, chat: user_level(source, chat) >= int(level)

## MUC & Roster handlers.
def send_join_presece(conf, nick, code = None):
	for User in GROUPCHATS[conf].values():
		User["ishere"] = False
	Presence = xmpp.protocol.Presence('%s/%s' % (conf, nick))
	Presence.setStatus(STATUS[conf]['message'])
	Presence.setShow(STATUS[conf]['status'])
	Presence.setTag('c', namespace = xmpp.NS_CAPS, attrs = {'node': Caps, 'ver': CapsVer})
	xTag = Presence.setTag('x', namespace = xmpp.NS_MUC)
	xTag.addChild('history', {'maxchars': '0'})
	if code:
		xTag.setTagData('password', code)
	jClient.send(Presence)

def join_groupchat(conf, nick, code = None):
	call_sfunctions("01si", (conf,))
	if conf not in GROUPCHATS:
		GROUPCHATS[conf] = {}
	if conf not in STATUS:
		STATUS[conf] = {'message': 'BlackSmith, XMPP BOT, is ready to work.', 'status': 'chat'}
	save_conflist(conf, nick, code)
	send_join_presece(conf, nick, code)
	Print("joined %s" % (conf), color3)

def leave_groupchat(chat, status = None):
	Presence = xmpp.Presence(chat, 'unavailable')
	if status:
		Presence.setStatus(status)
	jClient.send(Presence)
	if chat in GROUPCHATS:
		del GROUPCHATS[chat]
	call_sfunctions("04si", (chat,))
	save_conflist(chat)

def handler_rebody(target, body, ltype):
	col, all = 0, str(len(body) / PRIV_MSG_LIMIT + 1)
	while len(body) > PRIV_MSG_LIMIT:
		col = col + 1
		text = u'[%d/%s] %s[...]' % (col, all, body[:PRIV_MSG_LIMIT])
		jClient.send(xmpp.Message(target, text.strip(), ltype))
		body = body[PRIV_MSG_LIMIT:]
		time.sleep(2)
	return u'[%d/%s] %s' % ((col + 1), all, body)

def delivery(body):
	INFO["outmsg"] += 1
	if INFO.get("creporter"):
		try:
			jClient.send(xmpp.Message(BOSS, body, 'chat'))
		except:
			print_exc()
			write_file("delivery.txt", body, "a")

def msg(target, body):
	jid = str(target).split("/")[0]
	if GROUPCHATS.has_key(target):
		mType = "groupchat"
		if len(body) > CHAT_MSG_LIMIT:
			MORE[target] = body[CHAT_MSG_LIMIT:].strip()
			body = (u'%s[...]\n\n*** Лимит %d знаков! Продолжение по команде «далее».' % (body[:CHAT_MSG_LIMIT].strip(), CHAT_MSG_LIMIT))
	else:
		mType = "chat"
		if len(body) > PRIV_MSG_LIMIT:
			body = handler_rebody(target, body, mType)
	INFO["outmsg"] += 1
	jClient.send(xmpp.Message(target, body.strip(), mType))

def reply(mType, source, body):
	if mType in ("public", "groupchat"):
		body = "%s: %s" % (source[2], body)
		msg(source[1], body)
	elif mType in ("private", "chat"):
		msg(source[0], body)

def send_unavailable(status):
	Presence = xmpp.Presence(None, 'unavailable')
	Presence.setStatus(status)
	jClient.send(Presence)

def change_bot_status(conf, text, status):
	Presence = xmpp.protocol.Presence('%s/%s' % (conf, handler_botnick(conf)))
	Presence.setStatus(text)
	Presence.setShow(status)
	Presence.setTag('c', namespace = xmpp.NS_CAPS, attrs = {'node': Caps, 'ver': CapsVer})
	jClient.send(Presence)

def IQSender(chat, attr, data, afrls, role, text = str(), handler = ()):
	stanza = xmpp.Iq(to = chat, typ = "set")
	query = xmpp.Node("query")
	query.setNamespace(xmpp.NS_MUC_ADMIN)
	arole = query.addChild("item", {attr: data, afrls: role})
	if text:
		arole.setTagData("reason", text)
	stanza.addChild(node = query)
	if not handler:
		jClient.send(stanza)
	else:
		handler, args = handler
		jClient.SendAndCallForResponse(stanza, handler, args)
	INFO["outiq"] += 1

## Affiliations.
def outcast(chat, jid, text = str(), handler = ()):
	IQSender(chat, "jid", jid, "affiliation", "outcast", text, handler)

def none(chat, jid, text = str(), handler = ()):
	IQSender(chat, "jid", jid, "affiliation", "none", text, handler)

def member(chat, jid, text = str(), handler = ()):
	IQSender(chat, "jid", jid, "affiliation", "member", text, handler)

def admin(chat, jid, text = str(), handler = ()):
	IQSender(chat, "jid", jid, "affiliation", "admin", text, handler)

def owner(chat, jid, text = str(), handler = ()):
	IQSender(chat, "jid", jid, "affiliation", "owner", text, handler)

## Roles.
def kick(chat, nick, text = str(), handler = ()):
	IQSender(chat, "nick", nick, "role", "none", text, handler)

def visitor(chat, nick, text = str(), handler = ()):
	IQSender(chat, "nick", nick, "role", "visitor", text, handler)

def participant(chat, nick, text = str(), handler = ()):
	IQSender(chat, "nick", nick, "role", "participant", text, handler)

def moderator(chat, nick, text = str(), handler = ()):
	IQSender(chat, "nick", nick, "role", "moderator", text, handler)

def roster_check(instance, body):
	if instance not in ANSWER:
		QA = random.choice(QUESTIONS.keys())
		ANSWER[instance] = {'key': QUESTIONS[QA]['answer'], 'tryes': 0}
		msg(instance, u'Привет! Мне нужно убедиться, что ты не бот: %s. У тебя три попытки и 1 минута!' % (QUESTIONS[QA]['question']))
		try:
			composeTimer(60, roster_timer, None, (instance,)).start()
		except:
			pass
	elif ANSWER[instance]['tryes'] >= 3:
		roster_ban(instance)
	elif ANSWER[instance]['key'] == body.lower():
		RSTR['AUTH'].append(instance)
		write_file(ROSTER_FILE, str(RSTR))
		msg(instance, u'Правильно!')
		jClient.Roster.Authorize(instance)
		jClient.Roster.Subscribe(instance)
		jClient.Roster.setItem(instance, instance, ['USERS'])
		del ANSWER[instance]
		delivery(u'Контакт %s прошел IQ проверку и был добавлен в группу "USERS"!' % (instance))
	else:
		ANSWER[instance]['tryes'] += 1
		msg(instance, u'Включи мозг! Неправильно!')

def roster_ban(instance):
	if not '@conf' in instance:
		RSTR['BAN'].append(instance)
		write_file(ROSTER_FILE, str(RSTR))
		msg(instance, u'Поздравляю, ты в бане!')
		jClient.Roster.Unsubscribe(instance)
		if instance in jClient.Roster.getItems():
			jClient.Roster.delItem(instance)
		del ANSWER[instance]
		delivery(u'Контакт %s не прошел IQ проверку и был добавлен в ростер бан!' % (instance))

def roster_timer(roster_user):
	if roster_user not in (RSTR['AUTH'] + RSTR['BAN']):
		roster_ban(roster_user)

def CheckFlood():
	Flood.append(time.time())
	if len(Flood) > 4:
		if (Flood[-1] - Flood[0]) < 9:
			globals()["Flood"] = [Flood.pop()]
			raise xmpp.NodeProcessed()
		else:
			Flood.pop(0)

def MESSAGE_PROCESSING(client, stanza):
	source = stanza.getFrom()
	INFO['msg'] += 1
	instance = source.getStripped().lower()
	if user_level(source, instance) < -99:
		raise xmpp.NodeProcessed()
	isConf = (instance in GROUPCHATS)
	if not isConf and not has_access(source, 80, instance):
		if RSTR['VN'] == 'off':
			raise xmpp.NodeProcessed()
		CheckFlood()
	if (instance in UNAVAILABLE and not MSERVE) or stanza.getTimestamp(): #"""Warning: i think these terms may cause problems"""
		raise xmpp.NodeProcessed()
	bot_nick = handler_botnick(instance)
	nick = source.getResource()
	if bot_nick == nick:
		raise xmpp.NodeProcessed()
	Subject = isConf and stanza.getSubject()
	body = stanza.getBody()
	if body:
		body = body.strip()
	elif Subject:
		body = Subject.strip()
	else: ##if not body:
		raise xmpp.NodeProcessed()
	if not isConf and instance not in ADLIST:
		if not '@conf' in instance:
			if instance in RSTR['BAN'] or RSTR['VN'] == 'off':
				raise xmpp.NodeProcessed()
			elif instance not in RSTR['AUTH'] and RSTR['VN'] == 'iq':
				sThread("rIQ", roster_check, (instance, body))
				raise xmpp.NodeProcessed()
	if len(body) > INC_MSG_LIMIT:
		body = "%s[...] %d symbols limit." % (body[:INC_MSG_LIMIT].strip(), INC_MSG_LIMIT)
	stype = stanza.getType()
	if stype == 'error':
		code = stanza.getErrorCode()
		if code in ('500', '406'):
			if code == '406':
				if not isConf:
					raise xmpp.NodeProcessed()
				send_join_presece(instance, bot_nick)
				time.sleep(0.6)
			msg(source, body)
		raise xmpp.NodeProcessed()
	if Subject:
		call_efunctions("09eh", (instance, nick, Subject, body))
	else:
		if stype != 'groupchat':
			if (stanza.getTag('request')):
				answer = xmpp.Message(source)
				answer.setTag("received", namespace = xmpp.NS_RECEIPTS).setAttr("id", stanza.getID())
				answer.setID(stanza.getID())
				jClient.send(answer)
			type = 'private'
		else:
			type = 'public'
			if isConf and nick in GROUPCHATS[instance]:
				GROUPCHATS[instance][nick]['idle'] = time.time()
		command, Parameters, combody = '', '', body
		for app in [bot_nick+key for key in (':', ',', '>')]:
			if combody.startswith(app):
				combody = combody[len(app):].lstrip()
				break
		if not combody:
			raise xmpp.NodeProcessed()
		cmd = combody.split()[0].lower()
		if instance in COMMOFF and cmd in COMMOFF[instance]:
			raise xmpp.NodeProcessed()
		combody = MACROS.expand(combody, [source, instance, nick])
		if instance in MACROS.macrolist.keys():
			cmds = MACROS.gmacrolist.keys() + MACROS.macrolist[instance].keys()
		else:
			cmds = MACROS.gmacrolist.keys()
		if not combody:
			raise xmpp.NodeProcessed()
		combody = combody.split(None, 1)
		command = combody.pop(0).lower()
		if instance in PREFIX and cmd not in cmds:
			NotPfx = Prefix_state(body, bot_nick)
			if NotPfx or stype == 'chat':
				if not COMMANDS.has_key(command) and command.startswith(cPrefs):
					command = command[1:]
			else:
				command = command_Prefix(instance, command)
		if instance in COMMOFF and command in COMMOFF[instance]:
			raise xmpp.NodeProcessed()
		if COMMANDS.has_key(command):
			if combody:
				Parameters = combody.pop()
			INFO['cmd'] += 1
			LAST['cmd'] = u"Помощь по командам: «хелп» (последнее действие — «%s»)." % (command)
			call_command_handlers(command, type, [source, instance, nick], Parameters, cmd)
			LAST['time'] = time.time()
		else:
			call_efunctions("01eh", (stanza, type, [source, instance, nick], body))

def status_code_change(items, chat, nick):
	for item in items:
		try:
			del GROUPCHATS[chat][nick][item]
		except KeyError:
			pass

def error_join_timer(chat):
	if chat in GROUPCHATS:
		send_join_presece(chat, handler_botnick(chat))

def roster_subscribe(jid):
	if jid in ADLIST:
		jClient.Roster.Authorize(jid)
		jClient.Roster.Subscribe(jid)
		jClient.Roster.setItem(jid, jid, ['Admins'])
	elif RSTR['VN'] == 'off':
		jClient.Roster.Unauthorize(jid)
		if jid in jClient.Roster.getItems():
			jClient.Roster.delItem(jid)
	elif not jid in RSTR['BAN'] and RSTR['VN'] in ('iq', 'on'):
		jClient.Roster.Authorize(jid)
		jClient.Roster.Subscribe(jid)
		jClient.Roster.setItem(jid, jid, ['Users'])

Roles = {'owner': 15, 'moderator': 15, 'participant': 10, 'admin': 5, 'member': 1}

def calc_acc(conf, jid, role):
	if not GLOBACCESS.has_key(jid):
		if not (CONFACCESS.has_key(conf) and CONFACCESS[conf].has_key(jid)):
			access = (Roles.get(role[0], 0) + Roles.get(role[1], 0))
			change_local_access(conf, jid, access)

def PRESENCE_PROCESSING(client, stanza):
	fromjid = stanza.getFrom()
	INFO['prs'] += 1
	conf = fromjid.getStripped().lower()
	if not has_access(fromjid, -5, conf):
		raise xmpp.NodeProcessed()
	Ptype = stanza.getType()
	if Ptype == 'subscribe':
		roster_subscribe(conf)
	if GROUPCHATS.has_key(conf):
		nick = fromjid.getResource()
		if Ptype == 'unavailable':
			reason = stanza.getReason() or stanza.getStatus()
			if GROUPCHATS[conf].has_key(nick) and GROUPCHATS[conf][nick]['ishere']:
				GROUPCHATS[conf][nick]['ishere'] = False
			scode = stanza.getStatusCode()
			if scode in ('301', '307') and nick == handler_botnick(conf):
				leave_groupchat(conf, u'Got %s code!' % str(scode))
				text = (u'забанили' if scode == '301' else u'кикнули')
				delivery(u'Меня %s в "%s" и я оттуда вышел.' % (text, conf))
				raise xmpp.NodeProcessed()
			elif scode == '303':
				full_jid = stanza.getJid()
				if not full_jid:
					full_jid = unicode(fromjid)
					jid = unicode(fromjid)
				else:
					full_jid = unicode(full_jid)
					jid = full_jid.split('/')[0].lower()
				Nick = stanza.getNick()
				try:
					GROUPCHATS[conf][Nick] = GROUPCHATS[conf].pop(nick)
				except KeyError:
					role = (stanza.getRole(), stanza.getAffiliation())
					Time = time.time()
					GROUPCHATS[conf][nick] = {"role": role, "caps": stanza.getTagAttr("c", "node"), 'full_jid': full_jid, 'jid': jid, 'join_date': (that_day(), time.gmtime()), 'idle': Time, 'joined': Time, 'ishere': True}
					calc_acc(conf, jid, role)
					status = stanza.getShow()
					text = stanza.getStatus()
					call_efunctions("04eh", (conf, nick, role[1], role[0], status, text))
				else:
					GROUPCHATS[conf][Nick]['idle'] = time.time()
					call_efunctions("06eh", (stanza, conf, nick, Nick))
			else:
				call_efunctions("05eh", (conf, nick, reason, scode)) #1
				status_code_change(('idle', 'joined', "caps"), conf, nick) #0
		elif Ptype in ('available', None):
			full_jid = stanza.getJid()
			if not full_jid:
				if MSERVE:
					if conf not in UNAVAILABLE:
						UNAVAILABLE.append(conf)
					jid = full_jid = unicode(fromjid)
				else:
					if conf not in UNAVAILABLE:
						UNAVAILABLE.append(conf)
						msg(conf, u'Отключаюсь до получения прав админа!')
						change_bot_status(conf, u'Отказываюсь работать без прав!', 'xa')
					raise xmpp.NodeProcessed()
			elif conf in UNAVAILABLE:
				if MSERVE:
					UNAVAILABLE.remove(conf)
					full_jid = unicode(full_jid)
					jid = full_jid.split("/", 1)[0].lower()
				else:
					if nick == handler_botnick(conf) and stanza.getAffiliation() in ('admin','owner'):
						UNAVAILABLE.remove(conf)
						msg(conf, u'Походу дали админа, перезахожу!')
						time.sleep(2)
						leave_groupchat(conf, 'Rejoin...')
						time.sleep(2)
						join_groupchat(conf, handler_botnick(conf))
					raise xmpp.NodeProcessed()
			else:
				full_jid = unicode(full_jid)
				jid = full_jid.split("/", 1)[0].lower()
			ishere, role = GROUPCHATS[conf].has_key(nick), (stanza.getRole(), stanza.getAffiliation())
			if not (ishere and GROUPCHATS[conf][nick]['jid'] == jid and GROUPCHATS[conf][nick]['ishere']):
				GROUPCHATS[conf][nick] = {"role": role, "caps": stanza.getTagAttr("c", "node"), 'full_jid': full_jid, 'jid': jid, 'join_date': (that_day(), time.gmtime()), 'idle': time.time(), 'joined': time.time(), 'ishere': True}
				calc_acc(conf, jid, role)
				status = stanza.getShow()
				text = stanza.getStatus()
				call_efunctions("04eh", (conf, nick, role[1], role[0], status, text))
			elif ishere and GROUPCHATS[conf][nick]["role"] != role:
				GROUPCHATS[conf][nick]["role"] = role
				calc_acc(conf, jid, role)
				call_efunctions("07eh", (conf, nick, role, stanza.getReason()))
			else:
				status = stanza.getShow()
				text = stanza.getStatus()
				priority = stanza.getPriority()
				call_efunctions("08eh", (conf, nick, status, priority, text))
		elif Ptype == 'error':
			ecode = stanza.getErrorCode()
			if ecode:
				if ecode == '409':
					BOT_NICKS[conf] = '%s.' % (nick)
					send_join_presece(conf, handler_botnick(conf))
				elif ecode in ('401', '403', '405'):
					leave_groupchat(conf, u'Got %s error code!' % str(ecode))
					delivery(u'Ошибка %s, пришлось выйти из «%s»' % (ecode, conf))
				elif ecode in ('404', '503'):
					try:
						ThrName = "rejoin-%s" % (conf.decode("utf-8"))
						if ThrName not in ThrNames():
							composeTimer(360, error_join_timer, ThrName, (conf,)).start()
					except:
						pass
		if GROUPCHATS.has_key(conf):
			call_efunctions("02eh", (stanza,))

def IQ_PROCESSING(client, iq):
	INFO["iq"] += 1
	fromjid = iq.getFrom()

	if not fromjid or user_level(fromjid, fromjid.getStripped().lower()) < -99:
		raise xmpp.NodeProcessed()

	if iq.getType() == "get":
			
		nsType = iq.getQueryNS()
		result = iq.buildReply("result")
		query = result.getTag("query")
		if nsType == xmpp.NS_VERSION:
			query.setTagData("name", "BlackSmith mark.1")
			query.setTagData("version", "%s (r.%s)" % (CORE_MODE, BOT_REV))
			query.setTagData("os", os_name)
		
		elif nsType == xmpp.NS_DISCO_INFO:
			anode = result.getTag("query")
			anode.addChild("identity", {"category": "client",
										"type": "bot",
										"name": "BlackSmith"})
			for feature in XEPs:
				anode.addChild("feature", {"var": feature})

		elif nsType == xmpp.NS_LAST:
			last = time.time() - LAST['time']
			query.setAttr('seconds', int(last))
			query.setData(LAST['cmd'])

		elif nsType == xmpp.NS_TIME:
			LocTime = time.strftime("%a, %d %b %Y %H:%M:%S")
			GMTime = time.strftime("%Y%m%dT%H:%M:%S (GMT)", time.gmtime())
			tz = time.strftime("%Z")
			if BOT_OS == "nt":
				tz = tz.decode("cp1251")
			query.setTagData("utc", GMTime)
			query.setTagData("tz", tz)
			query.setTagData("display", LocTime)

		elif nsType == xmpp.NS_URN_TIME: #! TEST IT
			anode = result.addChild("time", namespace = xmpp.NS_URN_TIME)
			anode.setTagData("utc", strfTime("%Y-%m-%dT%H:%M:%SZ", False))
			TimeZone = (time.altzone if time.daylight else time.timezone)
			anode.setTagData("tzo", "%s%02d:%02d" % (((TimeZone < 0) and "+" or "-"),
												   abs(TimeZone) / 3600,
												   abs(TimeZone) / 60 % 60))

		client.send(result)
		raise xmpp.NodeProcessed()
	call_efunctions("03eh", (iq,))

## actions start.
def starting_actions():
	load_access_levels()
	form_admins_list()
	load_roster_config()
	load_quests()
	load_plugins()

def Connect():
	globals()['jClient'] = globals()['JCON'] = xmpp.Client(HOST, PORT)
	Print('\n\nConnecting...', color4)
	if SECURE:
		CONNECT = jClient.connect((SERVER, PORT), None, None, False)
	else:
		CONNECT = jClient.connect((SERVER, PORT), None, False, True)
	if CONNECT:
		if SECURE and CONNECT != 'tls':
			Print('\nWarning: unable to estabilish secure connection - TLS failed!', color2)
		else:
			Print('\nConnection is OK', color3)
		Print('Using: %s' % str(jClient.isConnected()), color4)
	else:
		Exit("\nCan't Connect.\nSleep for 30 seconds", 0, 30)
	Print('\nAuthentication plese wait...', color4)
	AUTHENT = jClient.auth(USERNAME, PASSWORD, RESOURCE)
	if AUTHENT:
		if AUTHENT != 'sasl':
			Print('\nWarning: unable to perform SASL auth. Old authentication method used!', color2)
		else:
			Print('Auth is OK', color3)
	else:
		Exit('\nAuth Error: %s %s\nMaybe, incorrect jid or password?' % (`jClient.lastErr`, `jClient.lastErrCode`), 0, 12)
	jClient.sendInitPresence()
	jClient.RegisterHandler(xmpp.NS_MESSAGE, MESSAGE_PROCESSING)
	jClient.RegisterHandler(xmpp.NS_PRESENCE, PRESENCE_PROCESSING)
	jClient.RegisterHandler(xmpp.NS_IQ, IQ_PROCESSING)
	Print('\n\nYahoo! I am online!', color3)

def calc_Timeout():
	Chats = len(GROUPCHATS.keys())
	if Chats < 16:
		Timeout = 8
	elif Chats > 48:
		Timeout = 0.2
	else:
		Timeout = round(7.8 - (Chats - 16)*0.2438, 4)
	return (0, Timeout)

def Dispatch_handler(Timeout = 8):
	try:
		Cycle = jClient.iter(Timeout)
		if not Cycle:
			INFO["zc"] += 1
			if INFO["zc"] > 15:
				raise IOError("Disconnected!")
	except xmpp.Conflict:
		Print('\n\nError: XMPP Conflict!', color2)
		call_sfunctions("03si")
		os._exit(0)
	except (xmpp.SystemShutdown, IOError):
		while not jClient.isConnected():
			Print("\n#-# Reconnecting.", color2)
			INFO["zc"] = 0
			Connect()
			try_sleep(6)
		join_chats()
	except xmpp.StreamError:
		pass
	except KeyboardInterrupt:
		print "INTRRUPTED"
		sys_exit('Interrupt (Ctrl+C)')

def Dispatch_fail():
	INFO["errs"] += 1
	error = format_exc()
	write_file("__main__.crash", error, "a")
	Print("\n\n#-# Dispatch fail!", color2)

def sys_exit(Reason = ""):
	Print('\n\n%s' % (Reason), color2)
	if jClient.isConnected():
		send_unavailable(Reason)
	if (time.time() - INFO['start']) >= 30:
		call_sfunctions("03si")
	Exit('\n\nRESTARTING...\n\nPress Ctrl+C to exit', 0, 30)

## Main.
def main():
	Print('\n\n--> BOT STARTED\n\n\nChecking PID...', color4)
	if os.path.exists(PID_FILE):
		CACHE = eval(read_file(PID_FILE))
		PID = CACHE['PID']
		if PID != BOT_PID:
			if BOT_OS == 'nt':
				kill = "TASKKILL /PID %d /T /f" % (PID)
				os.system(kill)
			else:
				killed = "PID: %d - has been killed!" % (PID)
				try:
					os.kill(PID, 9)
				except:
					killed = "Last PID wasn't detected!"
				Print(killed, color3)
			CACHE = {'PID': BOT_PID, 'START': time.time(), 'REST': []}
		else:
			CACHE['REST'].append(time.strftime('%d.%m.%Y (%H:%M:%S)'))
	else:
		CACHE = {'PID': BOT_PID, 'START': time.time(), 'REST': []}
	Print('\nBot\'s PID: %d' % (BOT_PID), color4)
	write_file(PID_FILE, str(CACHE))
	globals()['RUNTIMES'] = {'START': CACHE['START'], 'REST': CACHE['REST']}
	starting_actions()
	Connect()
	call_sfunctions("00si")
	join_chats()
	Print('\n\nBlackSmith is ready to work!\n\n', color3)
	INFO['start'] = time.time()
	composeThr(ClearMemory, ClearMemory.func_name).start()
	call_sfunctions("02si")
	Iters, Timeout = calc_Timeout()
	while True:
		if INFO["errs"] > 6:
			sys_exit("Fatal exception: %s\n" % (format_exc()))
		if Iters > 9000:
			Iters, Timeout = calc_Timeout()
		try:
			Dispatch_handler(Timeout)
		except IOError:
			sys_exit(format_exc())
		except:
			Dispatch_fail()
		Iters += 1

if __name__ == "__main__":
	while True:
		try:
			main()
		except KeyboardInterrupt:
			sys_exit('Interrupt (Ctrl+C)')
		except xmpp.HostUnknown:
			Print('\n\nError: host unknown!', color2)
		except:
			lytic_crashlog(main)
		try_sleep(6)

## That is all...