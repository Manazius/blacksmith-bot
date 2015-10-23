# BS mark.1-55
# coding: utf-8

#  BlackSmith compatibility with Talisman bot
#  __talisman__.py

# © simpleApps, 2012
#-extmanager-extVer:2.4.2-#
#-extmanager-conflict:extensions/talisman-pc.py-#

import traceback

GROUPCHAT_CACHE_FILE = GROUPCHATS_FILE
PLUGIN_DIR = "talisman"

## Config compability.
CONNECT_SERVER = SERVER
JID = "%s@%s" % (USERNAME, HOST)
ADMINS = [BOSS]
ADMIN_PASSWORD = (BOSS_PASS if BOSS_PASS else PASS_GENERATOR('', 128))
AUTO_RESTART = True

PUBLIC_LOG_DIR = ''
PRIVATE_LOG_DIR = ''
ACCBYCONF_FILE = ''

ROLES = {'none': 0, 'visitor': 0, 'participant': 10, 'moderator': 15}
AFFILIATIONS = {'none': 0, 'member': 0, 'admin': 5, 'owner': 15}

LAST.update({'c': '' , 't': 0, 'gch': {}})
BOT_VER = {'rev': BOT_REV, 'botver': {'name': 'BlackSmith', 'ver': 'mark.1 (r.%s)', 'os': os_name}}

MESSAGE_HANDLERS = Handlers["01eh"]
OUTGOING_MESSAGE_HANDLERS = []
JOIN_HANDLERS = Handlers["04eh"]
LEAVE_HANDLERS = Handlers["05eh"]
IQ_HANDLERS = Handlers["03eh"]
PRESENCE_HANDLERS = Handlers["02eh"]
STAGE0_INIT = Handlers["00si"]
STAGE1_INIT = Handlers["01si"]
STAGE2_INIT = Handlers["02si"]

ACCBYCONFFILE = CONFACCESS
GCHCFGS = {}

CMD_FLAG = False

smph = threading.Semaphore(30)
mtx = threading.Lock()
wsmph = Sequence

def write_file_gag(filename, data):
	pass

def register_talisman_handler(List, instance):
	Name = instance.func_name
	for inst in Handlers[List]:
		if inst.func_name == "Spike":
			if inst.TrueName == Name:
				Handlers[List].remove(inst)
	if List == "04eh":
		def Spike(a, b, c, d, e, f):
			instance(a, b, c, d)
	else:
		def Spike(*ls):
			instance(*ls)
	Spike.TrueName = Name
	Handlers[List].append(Spike)

def register_message_handler(instance):
	register_talisman_handler("01eh", instance)
def register_outgoing_message_handler(instance):
	name = instance.func_name
	for handler in OUTGOING_MESSAGE_HANDLERS:
		if name == handler.func_name:
			OUTGOING_MESSAGE_HANDLERS.remove(handler)
	OUTGOING_MESSAGE_HANDLERS.append(instance)
def register_join_handler(instance):
	register_talisman_handler("04eh", instance)
def register_leave_handler(instance):
	register_talisman_handler("05eh", instance)
def register_iq_handler(instance):
	register_talisman_handler("03eh", instance)
def register_presence_handler(instance):
	register_talisman_handler("02eh", instance)
def register_stage0_init(instance):
	execute_handler(instance)
def register_stage1_init(instance):
	register_talisman_handler("01si", instance)
def register_stage2_init(instance):
	register_talisman_handler("02si", instance)

def register_command_handler(instance, command, category = [], access = 0, desc = None, syntax = None, examples = []):
	command = command.decode('utf-8')
	if CMD_FLAG:
		if COMMANDS.has_key(command):
			command += "."
	if not COMMSTAT.has_key(command):
		COMMSTAT[command] = {'col': 0, 'users': []}
	COMMAND_HANDLERS[command] = instance
	COMMANDS[command] = {'access': access,
			'desc': desc.decode('utf-8'),
			'syntax': syntax.decode('utf-8'),
			'examples': [ex.decode('utf-8') for ex in examples]}

def call_message_handlers(*ls):
	call_efunctions("01eh", *ls)
def call_outgoing_message_handlers(*ls):
	for handler in OUTGOING_MESSAGE_HANDLERS:
		sThread(*ls)
def call_join_handlers(*ls):
	call_efunctions("04eh", *ls)
def call_leave_handlers(*ls):
	call_efunctions("05eh", *ls)
def call_iq_handlers(*ls):
	call_efunctions("03eh", *ls)
def call_presence_handlers(*ls):
	call_efunctions("02eh", *ls)

def find_plugins(dir = PLUGIN_DIR):
	Ok, Feil = [], []
	for ext in sorted(os.listdir(dir)):
		if ext.endswith(".py"):
			path = os.path.join(dir, ext)
			try:
				data = open(path).read(20)
			except:
				data = str()
			if data.count("talis"):
				Ok.append(ext)
			else:
				Feil.append(ext)
	return (Ok, Feil)

def load_talisman_plugins():
	if os.path.exists(PLUGIN_DIR):
		Print('\n\nLOADING TALISMAN PLUGINS:', color4)
		All = find_plugins()
		Ok, Feil = [], []
		for ext in All[0]:
			path = os.path.join(PLUGIN_DIR, ext)
			ext_name = os.path.splitext(ext)[0]
			try:
				execfile(path, globals()); Ok.append(ext_name)
			except:
				print_exc()
				Feil.append(ext_name)
		if Ok:
			Print('\n\nLoaded %d Talisman plugins:\n%s' % (len(Ok), ', '.join(sorted(Ok))), color3)
		if Feil:
			Print('\n\nThere are %d unloadable plugins:\n%s' % (len(Feil), ', '.join(sorted(Feil))), color2)
		else:
			Print('\n\nThere are not unloadable plugins!', color3)

def get_gch_cfg(gch):
	pass

def upkeep(): # deprecated
	pass

get_true_jid = handler_jid

get_bot_nick = handler_botnick

def get_gch_info(gch, info):
	pass

add_gch = save_conflist

##def change_bot_status(gch, status, show, auto = 0):
##	pass

def change_access_temp(gch, source, level = 0):
	pass

change_access_perm = change_local_access

def change_access_temp_glob(source, level = 0):
	pass

change_access_perm_glob = change_global_access

def isadmin(jid):
	return jid == BOSS

def findPresenceItem(node):
	for p in [x.getTag('item') for x in node.getTags('x', namespace = xmpp.NS_MUC_USER)]:
		if p != None:
			return p
	return None

messageHnd = MESSAGE_PROCESSING
presenceHnd = PRESENCE_PROCESSING
iqHnd = IQ_PROCESSING

def dcHnd():
	pass

start = main

order_kick = kick

order_visitor = visitor

order_ban = outcast

order_unban = none

def findAndReplace(mType, source, args):
	plugins = find_plugins("extensions")[0] # find talisman plugins in bs extensions
	args = args.strip()
	answer = str()
	if not args:
		answer = u"А параметры?"
	if args in ("move", u"переместить"):
		import shutil
		if not os.path.exists(PLUGIN_DIR):
			os.makedirs(PLUGIN_DIR)
		for plug in plugins:
			oldpath = os.path.join("extensions", plug)
			newpath = os.path.join(PLUGIN_DIR, plug)
			shutil.move(oldpath, newpath)
		del shutil
		answer = u"Успешно перемещено %d плагинов Talisman-bot." % len(plugins)
	elif args in ("exterminate", u"уничтожить"):
		for plug in plugins:
			addr = os.path.join("extensions", plug)
			os.remove(addr)
		answer = u"Успешно уничтожено %d плагинов Talisman-bot." % len(plugins)
	reply(mType, source, answer)

command_handler(findAndReplace, 100, "__talisman__")
handler_register("00si", load_talisman_plugins)

## compatibility up to 9000 (over 75%)