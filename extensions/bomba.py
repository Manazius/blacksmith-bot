# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  bomba.py

# Coded by: 40tman (40tman@qip.ru)
# ReCoded: by WitcherGeralt (WitcherGeralt@jabber.ru)

#-extmanager-extVer:1.3-# 

COLOR = [u'красный', u'зеленый', u'синий', u'голубенький', u'белый', u'желтый', u'серый', u'оранжевый', u'фиолетовый', u'серо-буро-малиновый']

PROVOD = {}

def bomb(type, source, args):
	if source[1] in GROUPCHATS:
		if args:
			nick = args.strip()
			if user_level(source[0], source[1]) < 15 and nick != source[2]:
				reply(type, source, u'ты можешь взрывать только себя')
				return
			if not nick in GROUPCHATS[source[1]] or not GROUPCHATS[source[1]][nick]['ishere']:
				reply(type, source, u'юзера с таким ником здесь нет')
				return
		else:
			nick = source[2]
		if user_level(source[1]+'/'+nick, source[1]) < 15:
			provoda = []
			for prv in COLOR:
				if len(provoda) < 2 or random.randrange(1, 10) >= 7:
					provoda.append(prv)
			provod = random.choice(provoda)
			PROVOD[nick] = provod
			time = random.randrange(15, 45)
			msg(source[1], nick+u': вам вручена бомба, на ней '+str(len(provoda))+u' провода(ов): '+', '.join(provoda)+u' выберите цвет провода который нужно перерезать, на таймере '+str(time)+u' секунд')
			try:
				threading.Timer(time, bomb_start,(source[1], nick)).start()
			except:
				pass
		else:
			reply(type, source, u'модеры не взрываются!')
	else:
		reply(type, source, u'ты дурак?')

def bomb_start(conf, nick):
	if nick in PROVOD and GROUPCHATS[conf][nick]['ishere']:
		kick(conf, nick, u'птыдыщь!')
		del PROVOD[nick]

def bomb_msg(raw, type, source, body):
	if source[2] in PROVOD:
		answer = body.lower()
		if answer == PROVOD[source[2]]:
			reply(type, source, u'бомба обезврежена!')
			del PROVOD[source[2]]
		else:
			kick(source[1], source[2], u'птыдыщь!')
			del PROVOD[source[2]]

handler_register("01eh", bomb_msg)

command_handler(bomb, 10, "bomba")
