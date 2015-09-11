# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith plugin
#  features_plugin.py

#  Initial Copyright © 2007 Als [Als@exploit.in]

features = {'http://jabber.ru/muc-filter': 'Chat`s defender','gc-1.0': 'XEP-0045: Multi-User Chat','http://jabber.org/protocol/activity': 'XEP-0108: User Activity','http://jabber.org/protocol/address': 'XEP-0033: Extended Stanza Addressing','http://jabber.org/protocol/amp': 'XEP-0079: Advanced Message Processing','http://jabber.org/protocol/bytestreams': 'XEP-0065: SOCKS5 Bytestreams','http://jabber.org/protocol/caps': 'XEP-0115: Entity Capabilities','http://jabber.org/protocol/chatstates': 'XEP-0085: Chat State Notifications','http://jabber.org/protocol/commands': 'XEP-0050: Ad-Hoc Commands','http://jabber.org/protocol/compress': 'XEP-0138: Stream Compression','http://jabber.org/protocol/disco': 'XEP-0030: Service Discovery','http://jabber.org/protocol/feature-neg': 'XEP-0020: Feature Negotiation','http://jabber.org/protocol/geoloc': 'XEP-0080: User Geolocation','http://jabber.org/protocol/http-auth': 'XEP-0072: SOAP Over XMPP','http://jabber.org/protocol/httpbind': 'XEP-0124: Bidirectional-streams Over Synchronous HTTP','http://jabber.org/protocol/ibb': 'XEP-0047: In-Band Bytestreams','http://jabber.org/protocol/mood': 'XEP-0107: User Mood','http://jabber.org/protocol/muc': 'XEP-0045: Multi-User Chat','http://jabber.org/protocol/offline': 'XEP-0013: Flexible Offline Message Retrieval','http://jabber.org/protocol/physloc': 'XEP-0080: User Geolocation','http://jabber.org/protocol/pubsub': 'XEP-0060: Publish-Subscribe','http://jabber.org/protocol/rosterx': 'XEP-0144: Roster Item Exchange','http://jabber.org/protocol/sipub': 'XEP-0137: Publishing SI Requests','http://jabber.org/protocol/soap': 'XEP-0072: SOAP Over XMPP','http://jabber.org/protocol/waitinglist': 'XEP-0130: Waiting Lists','http://jabber.org/protocol/xhtml-im': 'XEP-0071: XHTML-IM','http://jabber.org/protocol/xdata-layout': 'XEP-0141: Data Forms Layout','http://jabber.org/protocol/xdata-validate': 'XEP-0122: Data Forms Validation','ipv6': 'Support of IPv6','jabber:client': 'RFC 3921: XMPP IM','jabber:component:accept': 'XEP-0114: Existing Component Protocol','jabber:component:connect': 'XEP-0114: Existing Component Protocol','jabber:iq:auth': 'XEP-0078: Non-SASL Authentication','jabber:iq:browse': 'XEP-0011: Jabber Browsing','jabber:iq:gateway': 'XEP-0100: Gateway Interaction','jabber:iq:last': 'XEP-0012: Last Activity','jabber:iq:oob': 'XEP-0066: Out of Band Data','jabber:iq:pass': 'XEP-0003: Proxy Accept Socket Service','jabber:iq:privacy': 'RFC 3921: XMPP IM','jabber:iq:private': 'XEP-0049: Private XML Storage','jabber:iq:register': 'XEP-0077: In-Band Registration','jabber:iq:roster': 'RFC 3921: XMPP IM','jabber:iq:rpc': 'XEP-0009: Jabber-RPC','jabber:iq:search': 'XEP-0055: Jabber Search','jabber:iq:time': 'XEP-0202: Entity Time','jabber:iq:version': 'XEP-0092: Software Version','jabber:server': 'RFC 3921: XMPP IM','jabber:x:data': 'XEP-0004: Data Forms','jabber:x:delay': 'XEP-0203: Delayed Delivery','jabber:x:encrypted': 'XEP-0027: Current OpenPGP Usage','jabber:x:event': 'XEP-0022: Message Events','jabber:x:expire': 'XEP-0023: Message Expiration','jabber:x:oob': 'XEP-0066: Out of Band Data','jabber:x:roster': 'XEP-0093: Roster Item Exchange','jabber:x:signed': 'XEP-0027: Current OpenPGP Usage','urn:xmpp:delay': 'XEP-0203: Delayed Delivery','urn:xmpp:ping': 'XEP-0199: XMPP Ping','urn:xmpp:receipts': 'XEP-0199: XMPP Ping','urn:xmpp:ssn': 'XEP-0155: Stanza Session Negotiation','urn:xmpp:time': 'XEP-0202: Entity Time','vcard-temp': 'XEP-0054: vcard-temp'}

def handler_features_get(type, source, nick):
	if nick:
		if nick.count('@') and nick.count('/'):
			conf_nick = nick
		elif nick in GROUPCHATS[source[1]]:
			conf_nick = source[1]+'/'+nick
		else:
			reply(type, source, u'O_o !?')
			return
	else:
		conf_nick = source[0]
	iq = xmpp.Iq(to = conf_nick, typ = 'get')
	INFO['outiq'] += 1
	iq.addChild('query', {}, [], xmpp.NS_DISCO_INFO)
	jClient.SendAndCallForResponse(iq, handler_features_answer, {'type': type, 'source': source, 'nick': nick})

def handler_features_answer(coze, stanza, type, source, nick):
	if stanza:
		if stanza.getType() == 'result':
			feat = set()
			stanza = stanza.getQueryChildren()
			for x in stanza:
				att = x.getAttrs()
				if att.has_key('var'):
					attlist = att['var'].split()
					for x in attlist:
						for y in features:
							if x.count(y):
								feat.add(features[y])
			if feat:
				if nick:
					answer = u'Клиент %s держит:\n' % (nick)
				else:
					answer = u'Твой клиет держит следующие фичи:\n'
				if type == 'public':
					reply(type, source, u'ушли')
				reply('private', source, answer+'\n'.join(feat))
			else:
				reply(type, source, u'глючит клиент')

command_handler(handler_features_get, 10, "features")
