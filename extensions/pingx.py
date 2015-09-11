# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  pingx.py

# © (2004) Lars Strand

ICMP_DATA_STR = 56
ICMP_TYPE = 8
ICMP_TYPE_IP6 = 128
ICMP_CODE = 0
ICMP_CHECKSUM = 0
ICMP_ID = 0
ICMP_SEQ_NR = 0

def Packet_construct(id, size, ipv6):
	if size < int(struct.calcsize("d")):
		_error("packetsize to small, must be at least %d" % int(struct.calcsize("d")))
	if ipv6:
		header = struct.pack('BbHHh', ICMP_TYPE_IP6, ICMP_CODE, ICMP_CHECKSUM, ICMP_ID, ICMP_SEQ_NR+id)
	else:
		header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, ICMP_CHECKSUM, ICMP_ID, ICMP_SEQ_NR+id)
	load = "-- IF YOU ARE READING THIS YOU ARE A NERD! --"
	size -= struct.calcsize("d")
	rest = ""
	if size > len(load):
		rest = load
		size -= len(load)
	rest += size * "X"
	data = struct.pack("d", time.time())+rest
	checksummary = handler_in_cksummary(header+data)
	if ipv6:
		header = struct.pack('BbHHh', ICMP_TYPE_IP6, ICMP_CODE, checksummary, ICMP_ID, ICMP_SEQ_NR + id)
	else:
		header = struct.pack('bbHHh', ICMP_TYPE, ICMP_CODE, checksummary, ICMP_ID, ICMP_SEQ_NR + id)
	return header+data

def handler_in_cksummary(Packet):
	if len(Packet) & 1:
		Packet = Packet+'\0'
	words = array.array('h', Packet)
	summary = 0
	for word in words:
		summary += (word & 0xffff)
	hi = summary >> 16
	lo = summary & 0xffff
	summary = hi + lo
	summary = summary + (summary >> 16)
	return (~summary) & 0xffff

def PING_START(type, source, alive = 0, timeout = 1.0, ipv6 = 0, number = sys.maxint, node = None, flood = 0, size = ICMP_DATA_STR, status_only = 0):
	repl = ''
	if ipv6:
		if socket.has_ipv6:
			try:
				info, port = socket.getaddrinfo(node, None)
				host = info[4][0]
				if host == node:
					noPrintIPv6adr = 1
			except:
				repl +=  (u'Не могу найти %s: Неизвестный хост' % node)+'\n'
		else:
			repl +=  u'Недоступно IPv6 для на данной платформе\n'
	else:
		try:
			host = socket.gethostbyname(node)
		except:
			repl +=  (u'Не могу найти %s: Неизвестный хост' % node)+'\n'
	if not ipv6:
		try:
			if int(host.split(".")[-1]) == 0:
				repl +=  u'Нет поддержки пинга в сети'+'\n'
		except:
			repl +=  u'Пинг: ошибка, не корректный запрос'+'\n'
			host = '0.0.0.0'
	if number == 0:
		repl +=  (u'Ошибка количества пакетов на передачу: %s' % str(a))+'\n'
	if alive:
		number = 1
	start, mint, maxt, avg, lost, tsum, tsumsq = 1, 999, 0.0, 0.0, 0, 0.0, 0.0
	if not alive:
		if ipv6 and not status_only:
			if noPrintIPv6adr == 1:
				repl += (u'Пинг: %s : %d байты (40+8+%d)' % (str(node), 40 + 8 + size, size))+'\n'
			else:
				repl += (u'Пинг: %s (%s): %d байты (40+8+%d)' % (str(node), str(host), 40 + 8 + size, size))+'\n'
		elif not status_only:
			repl +=  (u'Пинг: %s (%s): %d байты (20+8+%d)' % (str(node), str(host), 20 + 8 + size, size))+'\n'
	try:
		while start <= number:
			lost += 1
			if ipv6:
				try:
					Psocket = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.getprotobyname("ipv6-icmp"))
				except socket.error, e:
					repl +=  u'Ошибка сокета: %s' % e+u' You must be root (%s uses raw sockets)' % os.path.basename(sys.argv[0])+'\n'
			else:
				try:
					Psocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname("icmp"))
				except socket.error, e:
					repl +=  u'Ошибка сокета: %s' % e+u' You must be root (%s uses raw sockets)' % os.path.basename(sys.argv[0])+'\n'

			Packet = Packet_construct(start, size, ipv6)
			try:
				Psocket.sendto(Packet,(node, 1))
			except socket.error, e:
				repl +=  u'Ошибка сокета: %s' % e+'\n'
			Pong, iwtd = "", []
			while True:
				iwtd, owtd, ewtd = select.select([Psocket], [], [], timeout)
				break
			if iwtd:
				endtime = time.time()
				Pong, address = Psocket.recvfrom(size + 48)
				lost -= 1
				if ipv6:
					PongHeader = Pong[0:8]
					PongType, PongCode, PongChksum, PongID, PongSeqnr = struct.unpack("bbHHh", PongHeader)
					starttime = struct.unpack("d", Pong[8:16])[0]
				else:
					rawPongHop = struct.unpack("s", Pong[8])[0]
					PongHop = int(binascii.hexlify(str(rawPongHop)), 16)
					PongHeader = Pong[20:28]
					PongType, PongCode, PongChksum, PongID, PongSeqnr = struct.unpack("bbHHh", PongHeader)
					starttime = struct.unpack("d", Pong[28:36])[0]
				if not PongSeqnr == start:
					Pong = None
			if not Pong:
				if alive and not status_only:
					repl +=  u'Нет ответа от %s (%s)' % (str(node), str(host))+'\n'
				elif alive and status_only:
					return u'Шняга какая-то!'
				else:
					repl +=  u'Пинг таймаут: %s (icmp_seq=%d) ' % (host, start)+'\n'
				if number != 1 and start < number:
					time.sleep(flood ^ 1)
				start += 1
				continue
			triptime  = endtime - starttime
			tsum += triptime
			tsumsq += triptime * triptime
			maxt = max ((triptime, maxt))
			mint = min ((triptime, mint))
			if alive and not status_only:
				repl +=  str(node)+' ('+str(host)+u') жив'+'\n'
			elif alive and status_only:
				return u'Шняга какая-то!'
			else:
				if ipv6:
					repl += u'%d байт от %s: #=%d время=%.5f ms' % (size + 8, host, PongSeqnr, triptime * 1000)+'\n'
				else:
					repl += u'%d байт от %s: #=%d ttl=%s время=%.5f мс' % (size + 8, host, PongSeqnr, PongHop, triptime* 1000)+'\n'
			if number != 1 and start < number:
				time.sleep(flood ^ 1)
			start += 1
	except (EOFError, KeyboardInterrupt):
		start += 1
	if start != 0 or lost > 0:
		start -= 1
		avg = tsum / start
		vari = tsumsq / start - avg * avg
		if start == lost:
			plost = 100
		else:
			plost = (lost/start)*100
		if not alive:
			repl += u'\n--- %s статистика пинга ---' % (node+'\n')
			repl += u'%d пакетов отправлено, %d пакетов принято, %d%% потеряно пакетов' % (start, start-lost, plost)+'\n'
			if plost != 100:
				repl += u'Итог мин./сред./макс./разн. = %.3f/%.3f/%.3f/%.3f мс' % (mint * 1000, (tsum/start) * 1000, maxt * 1000, math.sqrt(vari) * 1000)+'\n'
	try:
		Psocket.close()
	except:
		pass
	return repl

def handler_NetPING(type, source, body):
	import array, select, binascii, math, getopt, socket, struct
	if body:
		sicle, ipv6, flood, size = 1.0, 0, 0, ICMP_DATA_STR
		node = body.split()[0].strip()
		if body.count('-a'):
			alive = 1
		else:
			alive = 0
		if body.count('-c'):
			cis = body.split('-c=')[1].strip()
			ci = cis.split()[0].strip()
			if check_number(ci):
				count = int(ci)
			else:
				count = 3
		else:
			count = 3
		try:
			repl = PING_START(type, source, alive = alive, timeout = sicle, ipv6 = ipv6, number = count, node = node, flood = flood, size = size)
			if not repl:
				repl = u'Аблом!'
		except:
			repl = u'Аблом!'
		reply(type, source, repl)
	else:
		reply(type, source, u'Что пингуем?')
	del array, select, binascii, math, getopt, socket, struct

command_handler(handler_NetPING, 10, "pingx")
