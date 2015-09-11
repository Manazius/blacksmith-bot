# BS mark.1-55
# /* coding: utf-8 */
# Code © WitcherGeralt, 2012.
# Originally coded for BlackSmith mark.2


get_disp = lambda disp: "%s@%s" % (disp._owner.User, disp._owner.Server) if isinstance(disp, (xmpp.Client, xmpp.dispatcher.Dispatcher)) else disp

ALIVE_KEEPER = {}

def alive_keeper():

		def alive_keeper_answer(disp, stanza):
			if stanza:
				jClient.aKeeper = 0

		disp = jClient
		disp_str = get_disp(disp)
		while True:
			time.sleep(5)
			thrIds = [x.name for x in threading.enumerate()]
			if not hasattr(disp, "aKeeper"):
				disp.aKeeper = 0

			if disp.aKeeper > 2:
				disp.aKeeper = 0
				thrName = "alive-keeper"
				if thrName in thrIds:
					for thr in threading.enumerate():
						if thrName == thr.name:
							thr.kill()
				try:
					composeThr(Connect, thrName, ()).start()
				except Exception:
					lytic_crashlog(alive_keeper)

			else:
				disp.aKeeper += 1
				INFO["outiq"] += 1
				iq = xmpp.Iq("get", to="%s/%s" % (disp_str, RESOURCE))
				iq.addChild("ping", namespace=xmpp.NS_PING)
				iq.setID("Bs-i%d" % INFO["outiq"])
				jClient.SendAndCallForResponse(iq, alive_keeper_answer)



def conf_alive_keeper():

	def conf_alive_keeper_answer(disp, stanza, conf):
		if GROUPCHATS.has_key(conf) and ALIVE_KEEPER.has_key(conf):
			if xmpp.isErrorNode(stanza):
				if "405" == stanza.getErrorCode():
					ALIVE_KEEPER[conf] = 0
			else:
				ALIVE_KEEPER[conf] = 0

	while True:
		time.sleep(360)
		thrIds = [x.name for x in threading.enumerate()]
		for conf in GROUPCHATS.keys():

			if conf not in ALIVE_KEEPER:
				ALIVE_KEEPER[conf] = 0

			if ALIVE_KEEPER[conf] > 2:
				ALIVE_KEEPER[conf] = 0
				TimerName = "ejoinTimer-%s" % conf
				if TimerName not in thrIds:
					try:
						composeTimer(180, error_join_timer, TimerName, (conf,)).start()
					except Exception:
						lytic_crashlog(conf_alive_keeper)

			else:
				ALIVE_KEEPER[conf] += 1
				INFO["outiq"] += 1
				iq = xmpp.Iq("get", to = "%s/%s" % (conf, handler_botnick(conf)))
				iq.addChild("ping", namespace = xmpp.NS_PING)
				iq.setID("Bs-i%d" % INFO["outiq"])
				jClient.SendAndCallForResponse(iq, conf_alive_keeper_answer, {"conf": conf})


def start_keepers():
	Name1 = alive_keeper.__name__
	Name2 = conf_alive_keeper.__name__
	for thr in threading.enumerate():
		if thr.name.startswith((Name1, Name2)):
			thr.kill()
	composeThr(alive_keeper, Name1).start()
	composeThr(conf_alive_keeper, Name2).start()


handler_register("02si", start_keepers)