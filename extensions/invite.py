# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  invite.py

# © simpleApps, 2013.

inviteChatrooms = []

def command_sendInvite(mType, source, nick):
	chat = source[1]
	if chat in GROUPCHATS:
		if chat not in inviteChatrooms:	
			if nick:
				jid = None
				if "@" in nick or "." in nick:
					jid = nick
				elif nick in GROUPCHATS[chat]:
					jid = handler_jid("%s/%s" % (chat, nick))
				if jid:
					inviteChatrooms.append(chat)
					invite = xmpp.Message(to = chat)
					INFO["outmsg"] += 1
					x = xmpp.Node("x")
					x.setNamespace(xmpp.NS_MUC_USER)
					inv = x.addChild("invite", {"to": jid})
					inv.setTagData("reason", u"Вас приглашает %s" % source[2])
					invite.addChild(node = x)
					jClient.send(invite)
					reply(mType, source, u"Приглашение выслано!")
					composeTimer(180, lambda room: inviteChatrooms.remove(room), "inviteTimer-%s" % chat, (chat,)).start()
				else:
					reply(mType, source, u"Это не JabberID и пользователей с таким ником в базе нет.")
		else:
			reply(mType, source, u"Отсылать инвайты из одной конференции можно только один раз в течение 3-х минут.")
	else:
		reply(mType, source, u"Только для чатов!")


command_handler(command_sendInvite, 15, "invite")