# BS mark.1-55
# /* coding: utf-8 */
# © simpleApps, 27.11.2012.

# This plugin receives
# info about minecraft servers.
#-extmanager-extVer:1.2-#

import socket

def command_chkMinecraftServer(mType, source, argv):
	answer = u"что?"
	if argv:
		argv = argv.split()[:2]
		addr, port = str(), 25565
		if len(argv) == 1:
			addr = argv[0]
			if ":" in addr:
				addr, port = addr.split(":")
		elif len(argv) > 1:
			addr, port = argv
		else:
			reply(mType, source, answer)
			return
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(10)
		port = int(port)
		try:
			sock.connect((addr, port))
		except:
			answer = u"Не удалось подключиться к серверу."
		else:
			sock.send("\xFE")
			data = sock.recv(1024)
			if data:
				data = data[1:].decode("utf-16be")
				array = data.split(u"\xA7")
				Name, Online, Max = array
				Name = Name[1:]
				answer =u"\nИмя: %s\nКоличество игроков: %s\nМаксимум игроков: %s." % (Name, Online, Max)
	reply(mType, source, answer)

command_handler(command_chkMinecraftServer, 11, "minecraft")