# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  note_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

note_file = 'dynamic/notepad.txt'

def handler_note(type, source, body):
	NOTE = eval(read_file(note_file))
	jid = handler_jid(source[0])
	if body:
		args = body.split()
		check = args[0].strip()
		if check.lower() == u'чисть':
			NOTE[jid] = {}
			write_file(note_file, str(NOTE))
			reply(type, source, u'блокнот зачищен')
		elif len(args) >= 2:
			if check == '+':
				date = time.strftime('%d.%m.%Y (%H:%M:%S)', time.gmtime())
				text = body[(body.find(' ') + 1):].strip()
				if len(text) <= 512:
					if jid not in NOTE:
						NOTE[jid] = {}
					if len(NOTE[jid]) <= 16:
						for number in range(1, 17):
							if str(number) not in NOTE[jid]:
								NOTE[jid][str(number)] = date+'\n'+text
								break
						write_file(note_file, str(NOTE))
						reply(type, source, u'записано')
					else:
						reply(type, source, u'ты превысил лимит записей (16)')
				else:
					reply(type, source, u'слишком много текста для 1й записи (лимит 512 знаков)')
			elif check == '-':
				text = args[1].strip()
				if check_number(text):
					if jid in NOTE.keys():
						if text in NOTE[jid]:
							del NOTE[jid][text]
							write_file(note_file, str(NOTE))
							reply(type, source, u'удалено')
						else:
							reply(type, source, u'нет такой записи')
					else:
						reply(type, source, u'в блокноте нет твоих записей!')
				else:
					reply(type, source, u'это вообще не число!')
			else:
				reply(type, source, u'вообще чёто не то говоришь')
		else:
			reply(type, source, u'недобор аргументов')
	elif jid in NOTE and NOTE[jid] != {}:
		repl, list = '', sorted(NOTE[jid].items(), lambda x,y: int(x[0]) - int(y[0]))
		for x, z in list:
			repl += x+') '+z+'\n'
		reply(type, source, '\n'+repl.strip())
	else:
		reply(type, source, u'у тебя нет записей в блокноте')

def note_file_init():
	if not initialize_file(note_file):
		Print('\n\nError: can`t create notepad.txt!', color2)

command_handler(handler_note, 10, "note")
handler_register("00si", note_file_init)
