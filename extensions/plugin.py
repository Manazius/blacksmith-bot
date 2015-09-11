# BS mark.1-55
# coding: utf-8

#  BlackSmith mark.1
#  plugin.py

#  Copyleft

OUT_COMMANDS = {}

def handler_out_list(type, source):
	if OUT_COMMANDS:
		repl = u'Список отключённых команд: '+', '.join(sorted(OUT_COMMANDS.keys()))
	else:
		repl = u'Оключённых команд нет!'
	reply(type, source, repl)

def handler_command_out(type, source, body):
	if body:
		command = body.lower()
		if command in COMMANDS:
			OUT_COMMANDS[command] = COMMANDS[command]
			del COMMANDS[command]
			reply(type, source, u'Команда "%s" глобально отключена' % (command))
		else:
			reply(type, source, u'нет такой команды')
	else:
		handler_out_list(type, source)

def handler_from_out_com(type, source, body):
	if body:
		command = body.lower()
		if command in OUT_COMMANDS:
			COMMANDS[command] = OUT_COMMANDS[command]
			del OUT_COMMANDS[command]
			reply(type, source, u'Команда "%s" включена' % (command))
		else:
			reply(type, source, u'в базе возврата нет этой команды')
	else:
		handler_out_list(type, source)

def handler_plug_list(type, source, body):
	Ok, Feil = [], []
	for ext in sorted(os.listdir(EXT_DIR)):
		if ext.endswith(".py"):
			path = os.path.join(EXT_DIR, ext)
			try:
				data = open(path).read(20)
			except:
				data = str()
			ext_name = ext.split(".")[0]
			if data.count("# BS mark.1-55"):
				Ok.append(ext_name)
			else:
				Feil.append(ext_name)
	if body == 'get_valid_plugins':
		return sorted(Ok)
	else:
		repl = ''
		if Ok:
			repl += u"\nДоступно %d плагинов BlackSmith'а:\n%s" % (len(Ok), ', '.join(sorted(Ok)))
		if Feil:
			repl += u"\nВнимание! Вналичии %d недоступных плагинов:\n%s" % (len(Feil), ', '.join(sorted(Feil)))
		reply(type, source, repl)

def handler_load_plugin(type, source, body):
	if body:
		ext = body.lower()
		if ext in handler_plug_list(type, source, 'get_valid_plugins'):
			try:
				execfile('%s/%s.py' % (EXT_DIR, ext), globals())
				repl = u'Плагин %s был успешно подгружен!' % (ext)
			except:
				repl = u'Плагин %s не был подгружен!\nОшибка: %s' % (ext, returnExc())
		else:
			repl = u'Этот плагин не был найден в списке'
	else:
		repl = u'Если не знаешь, что подгрузить, то посмотри список плагинов (команда: плаглист)'
	reply(type, source, repl)

command_handler(handler_from_out_com, 100, "plugin")
command_handler(handler_command_out, 100, "plugin")
command_handler(handler_plug_list, 80, "plugin")
command_handler(handler_load_plugin, 100, "plugin")
