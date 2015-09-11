# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  commoff_plugin.py

#  Initial Copyright © 2007 Als [Als@exploit.in]
#  Modifications: WitcherGeralt [WitcherGeralt@rocketmail.com]

NACMD = [u'доступ', u'логин', u'логаут', u'доступ_лок', u'свал', u'команды', u'отключить', u'включить', u'комлист', u'хтобыл', u'хдея', u'хелп', u'комдоступ', u'суперадмину', u'тест']

def handler_commoff(type, source, body):
	if source[1] in GROUPCHATS:
		sadcmd, nsadcmd, valcomm, notvalcomm, alrcomm, npcomm, vcnt, ncnt, acnt, nocnt, repl = '', 0, '', '', '', '', 0, 0, 0, 0, ''
		if source[1] in COMMOFF:
			commoff = COMMOFF[source[1]]
		else:
			commoff = []
		if body:
			commands = body.split()
			for cmd in commands:
				if cmd in COMMANDS or cmd in cmd in MACROS.gmacrolist or MACROS.macrolist[source[1]]:
					if cmd in COMMANDS:
						access = COMMANDS[cmd]['access']
					if cmd in MACROS.gmacrolist:
						access = MACROS.gaccesslist[cmd]
					if cmd in MACROS.macrolist[source[1]]:
						access = MACROS.accesslist[source[1]][cmd]
					else:
						access = 0
					if user_level(source[0], source[1]) > access:
						if not cmd in NACMD:
							if not cmd in commoff:
								if not source[1] in COMMOFF:
									COMMOFF[source[1]] = []
								COMMOFF[source[1]].append(cmd)
								vcnt += 1
								valcomm += str(vcnt)+') '+cmd+'\n'
							else:
								acnt += 1
								alrcomm += str(acnt)+') '+cmd+'\n'
						else:
							ncnt += 1
							npcomm += str(ncnt)+') '+cmd+'\n'
					else:
						nsadcmd += 1
						sadcmd += str(nsadcmd)+') '+cmd+'\n'
				else:
					nocnt += 1
					notvalcomm += str(nocnt)+') '+cmd+'\n'
			if valcomm:
				repl += u'для этой конфы были отключены следующие команды:\n'+valcomm
			if alrcomm:
				repl += u'\nследующие команды не были отключены, поскольку они уже отключены:\n'+alrcomm
			if notvalcomm:
				repl += u'\nперечисленные ниже команды вообще не команды :) :\n'+notvalcomm
			if sadcmd:
				repl += u'\nследующие команды ты отключить не можеш, так как доступ отключаемых команд должен быть ниже твоего:\n'+sadcmd
			if npcomm:
				repl += u'\nследующие команды отключать вообще нельзя:\n'+npcomm
			if vcnt != 0:
				write_file('dynamic/'+source[1]+'/commoff.txt', str(COMMOFF[source[1]]))
		else:
			for cmd in commoff:
				vcnt += 1
				valcomm += str(vcnt)+') '+cmd+'\n'
			if valcomm:
				repl = u'В этой конфе отключены следующие команды:\n'+valcomm
			else:
				repl = u'В этой конфе включены все команды'
	else:
		repl = u'Ты не в конференции придурок!'
	reply(type, source, repl.strip())

def handler_common(type, source, body):
	if source[1] in GROUPCHATS:
		valcomm, notvalcomm, alrcomm, npcomm, vcnt, ncnt, acnt, nocnt, repl = '', '', '', '', 0, 0, 0, 0, ''
		if source[1] in COMMOFF:
			commoff = COMMOFF[source[1]]
		else:
			commoff = []
		if body:
			commands = body.split()
			for cmd in commands:
				if cmd in COMMANDS or cmd in cmd in MACROS.gmacrolist or MACROS.macrolist[source[1]]:
					if not cmd in NACMD:
						if cmd in commoff:
							COMMOFF[source[1]].remove(cmd)
							vcnt += 1
							valcomm += str(vcnt)+') '+cmd+'\n'
						else:
							acnt += 1
							alrcomm += str(acnt)+') '+cmd+'\n'
					else:
						ncnt += 1
						npcomm += str(ncnt)+') '+cmd+'\n'
				else:
					nocnt += 1
					notvalcomm += str(nocnt)+') '+cmd+'\n'
			if valcomm:
				repl += u'для этой конфы были включены следующие команды:\n'+valcomm
			if alrcomm:
				repl += u'\nследующие команды не были включены, поскольку они не были отключены:\n'+alrcomm
			if notvalcomm:
				repl += u'\nперечисленные ниже команды вообще не команды :) :\n'+notvalcomm
			if npcomm:
				repl += u'\nследующие команды не отключаются вообще:\n'+npcomm
			if vcnt != 0:
				write_file('dynamic/'+source[1]+'/commoff.txt', str(COMMOFF[source[1]]))
		else:
			repl = u'Ну и что ты хочеш от меня?'
	else:
		repl = u'Ты не в конференции придурок!'
	reply(type, source, repl)

def get_commoff(conf):
	if check_file(conf, 'commoff.txt', '[]'):
		COMMOFF[conf] = eval(read_file('dynamic/'+conf+'/commoff.txt'))
	else:
		delivery(u'Внимание! Не удалось создать commoff.txt для "%s"!' % (conf))

command_handler(handler_commoff, 20, "commoff")
command_handler(handler_common, 20, "commoff")

handler_register("01si", get_commoff)
