# BS mark.1-55
# /* coding: utf-8 */
# Code © WitcherGeralt, 2012.
# Originally coded for BlackSmith mark.2
# Rewritten in 2023

ALIVE_KEEPER = {}
GLOBAL_KEEPALIVE_TIMEOUT = 60
CHAT_KEEPALIVE_TIMEOUT = 60
CLIENT_TYPES = (xmpp.Client, xmpp.dispatcher.Dispatcher)


class alive_keeper(object):

	def __init__(self):
		self.global_keeper_cnt = 0
		self.looping = True

	get_disp = lambda self, jClient: "%s@%s" % (jClient._owner.User, jClient._owner.Server)\
		if isinstance(jClient, CLIENT_TYPES) else jClient

	def start_all(self):
		composeThr(self.alive_keeper, "alive-keeper").start()
		composeThr(self.alive_keeper_chat, "alive-keeper-groupchat").start()

	def alive_keeper(self):

		self.global_keeper_cnt = 0

		def alive_keeper_answer(jClient, stanza):
			if stanza:
				self.global_keeper_cnt = 0

		while self.looping:
			time.sleep(GLOBAL_KEEPALIVE_TIMEOUT)
			thr_ids = [x.name for x in threading.enumerate()]

			if self.global_keeper_cnt > 2:
				self.global_keeper_cnt = 0
				thread_name = "alive-keeper"
				if thread_name in thr_ids:
					for thr in threading.enumerate():
						if thread_name == thr.name:
							thr.kill()
				try:
					self.looping = False
					Exit("Looks like we're disconnected", 0, 5)
				except Exception:
					lytic_crashlog(self.alive_keeper)

			else:
				self.global_keeper_cnt += 1
				INFO["outiq"] += 1
				jid = xmpp.JID(node=USERNAME, domain=SERVER, resource=RESOURCE)
				iq = xmpp.Iq("get", to=str(jid))
				iq.addChild("ping", namespace=xmpp.NS_PING)
				iq.setID("Bs-i%d" % INFO["outiq"])
				jClient.SendAndCallForResponse(iq, alive_keeper_answer)


	def alive_keeper_chat(self):

		def chat_alive_keeper_answer(jClient, stanza, chat):
			if GROUPCHATS.has_key(chat) and ALIVE_KEEPER.has_key(chat):
				if xmpp.isErrorNode(stanza):
					if stanza.getErrorCode() == "405":
						ALIVE_KEEPER[chat] = 0
				else:
					ALIVE_KEEPER[chat] = 0

		while self.looping:
			time.sleep(CHAT_KEEPALIVE_TIMEOUT)
			thr_ids = [thr.name for thr in threading.enumerate()]
			for chat in GROUPCHATS.keys():

				if chat not in ALIVE_KEEPER:
					ALIVE_KEEPER[chat] = 0

				if ALIVE_KEEPER[chat] > 2:
					ALIVE_KEEPER[chat] = 0
					timer_name = "ejoinTimer-%s" % chat
					if timer_name not in thr_ids:
						try:
							composeTimer(180, error_join_timer, timer_name, (chat,)).start()
						except Exception:
							lytic_crashlog(chat_alive_keeper)

				else:
					ALIVE_KEEPER[chat] += 1
					INFO["outiq"] += 1
					iq = xmpp.Iq("get", to="%s/%s" % (chat, handler_botnick(chat)))
					iq.addChild("ping", namespace=xmpp.NS_PING)
					iq.setID("Bs-i%d" % INFO["outiq"])
					jClient.SendAndCallForResponse(iq, chat_alive_keeper_answer, {"chat": chat})


def start_keepers():
	keeper = alive_keeper()
	keeper.start_all()


handler_register("02si", start_keepers)