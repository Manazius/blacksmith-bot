# BS mark.1-55
# coding: utf-8

#  BlackSmith plugin
#  config_plugin.py

# Coded by: WitcherGeralt (WitcherGeralt@jabber.ru)
# http://witcher-team.ucoz.ru/

CONFIG = u"""# coding: utf-8

# BlackSmith general configuration file

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Jabber server to connect
SERVER = '%SERV%'

# Connecting Port
PORT = %PORT%

# Jabber server`s connecting Host
HOST = '%HOST%'

# Using TLS (True - to enable, False - to disable)
SECURE = %SECURE%

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# User`s account
USERNAME = '%USER%'

# Jabber ID`s Password
PASSWORD = '%PASS%'

# Resourse (please don`t touch it)
RESOURCE = u'%RES%'# You may write ru symbols here

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# Default chatroom nick
DEFAULT_NICK = u'%NICK%'# You may write ru symbols here

# Groupchat message size limit
CHAT_MSG_LIMIT = %CML%

# Private/Roster message size limit
PRIV_MSG_LIMIT = %PML%

# Incoming message size limit
INC_MSG_LIMIT = %IML%

# Working without rights of moder (True - to enable, False - to disable)
MSERVE = %WMW%

# Jabber account of bot`s owner
BOSS = '%BOSS%'

# Memory usage limit (size in kilobytes, 0 - not limited)
MEMORY_LIMIT = %MLT%

# Admin password, used as a key to command "login"
BOSS_PASS = '%BPS%'# % PASS_GENERATOR('', 14)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
"""

def handler_config(type, source, body):
	if body:
		config = {1: SERVER, 2: PORT, 3: HOST, 4: SECURE, 5: USERNAME, 6: PASSWORD, 7: RESOURCE, 8: DEFAULT_NICK, 9: CHAT_MSG_LIMIT, 10: PRIV_MSG_LIMIT, 11: INC_MSG_LIMIT, 12: MSERVE, 13: BOSS, 14: BOSS_PASS, 15: MEMORY_LIMIT}
		if body != '*':
			items = body.split()
			for item in items:
				if item.count('='):
					spls = item.split('=')
					if len(spls) == 2:
						if check_number(spls[0]):
							num = int(spls[0])
							if num >= 1 and num <= 15:
								if num in [2, 9, 10, 11, 15]:
									if check_number(spls[1]):
										number = int(spls[1])
										config[num] = number
										if num == 15:
											globals()['MEMORY_LIMIT'] = number
										elif num == 9:
											globals()['CHAT_MSG_LIMIT'] = number
										elif num == 10:
											globals()['PRIV_MSG_LIMIT'] = number
										elif num == 11:
											globals()['INC_MSG_LIMIT'] = number
								else:
									config[num] = spls[1]
		data, list = CONFIG, {'%SERV%': config[1], '%PORT%': str(config[2]), '%HOST%': config[3], '%SECURE%': str(config[4]), '%USER%': config[5], '%PASS%': config[6], '%RES%': config[7], '%NICK%': config[8], '%CML%': str(config[9]), '%PML%': str(config[10]), '%IML%': str(config[11]), '%WMW%': str(config[12]), '%BOSS%': config[13], '%BPS%': config[14], '%MLT%': str(config[15])}
		for key in list.keys():
			data = data.replace(key, list[key])
		if body != '*':
			write_file(GENERAL_CONFIG_FILE, unicode(data).encode('utf-8'))
		if type == 'public':
			reply(type, source, u'Есть! Отсылаю текущий конфинг в приват...')
		reply('private', source, data)
	else:
		if type == 'public':
			reply(type, source, u'смотри в приват')
		reply('private', source, u'\n1 - сервер\n2 - порт\n3 - хост\n4 - шифровка трафика\n5 - аккаунт\n6 - пароль от жида\n7 - ресурс\n8 - стандартный ник\n9 - лимит мессаг в чат\n10 - лимит приватных мессаг\n11 - лимит входящих мессаг\n12 - работа без прав\n13 - жид суперадмина\n14 - пароль босса\n15 - лимит оперативки')

command_handler(handler_config, 100, "config")
