# BS mark.1-55 plugin
# /* coding: utf-8 */

import socket

def command_dns(mType, source, address):
	if address:
		try:
			address = address.encode("idna")
			name, alias, addrs = socket.gethostbyaddr(address)
			addrs.insert(0, name)
			answer = ", ".join(addrs)
		except socket.error:
			try:
				answer = u"%s — %s" % (address, socket.gethostbyname(address))
			except socket.error:
				answer = "Нет ответа."
		reply(mType, source, answer)

def command_chkServer(mType, source, argv):
	answer = u"что?"	
	if argv:
		argv = argv.split()[:2]
		addr, port = str(), str()
		if len(argv) > 1:
			addr, port = argv
		elif ":" in argv[0]:
			addr, port = argv[0].split(":")
		else: 
			return reply(mType, source, answer)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(5)
		if port.isdigit():
			port = int(port)
		else:
			return reply(mType, source, answer)
		try:
			sock.connect((addr,port))
			answer = u"Порт %d на \"%s\" открыт." % (port, addr)
		except:
			answer = u"Порт %d на \"%s\" закрыт. Не достучался за 5 секунд." % (port, addr) 
		sock.close()
	reply(mType, source, answer)

command_handler(command_dns, 10, "dns")
command_handler(command_chkServer, 10, "dns")