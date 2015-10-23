# BS mark.1-55
# /* coding: utf-8 */
# © simpleApps, 29.11.2012.

# This plugin receives
# info about Teeworlds servers.
#-extmanager-extVer:1.4-#

import socket

flags = {"20": "AD",
			"784": "AE",
			"4": "AF",
			"28": "AG",
			"660": "AI",
			"8": "AL",
			"51": "AM",
			"24": "AO",
			"32": "AR",
			"16": "AS",
			"40": "AT",
			"36": "AU",
			"533": "AW",
			"248": "AX",
			"31": "AZ",
			"70": "BA",
			"52": "BB",
			"50": "BD",
			"56": "BE",
			"854": "BF",
			"100": "BG",
			"48": "BH",
			"108": "BI",
			"204": "BJ",
			"652": "BL",
			"60": "BM",
			"96": "BN",
			"68": "BO",
			"76": "BR",
			"44": "BS",
			"64": "BT",
			"72": "BW",
			"112": "BY",
			"84": "BZ",
			"124": "CA",
			"166": "CC",
			"180": "CD",
			"140": "CF",
			"178": "CG",
			"756": "CH",
			"384": "CI",
			"184": "CK",
			"152": "CL",
			"120": "CM",
			"156": "CN",
			"170": "CO",
			"188": "CR",
			"192": "CU",
			"132": "CV",
			"531": "CW",
			"162": "CX",
			"196": "CY",
			"203": "CZ",
			"276": "DE",
			"262": "DJ",
			"208": "DK",
			"212": "DM",
			"214": "DO",
			"12": "DZ",
			"218": "EC",
			"233": "EE",
			"818": "EG",
			"732": "EH",
			"232": "ER",
			"724": "ES",
			"231": "ET",
			"246": "FI",
			"242": "FJ",
			"238": "FK",
			"583": "FM",
			"234": "FO",
			"250": "FR",
			"266": "GA",
			"826": "GB",
			"308": "GD",
			"268": "GE",
			"254": "GF",
			"831": "GG",
			"288": "GH",
			"292": "GI",
			"304": "GL",
			"270": "GM",
			"324": "GN",
			"312": "GP",
			"226": "GQ",
			"300": "GR",
			"239": "GS",
			"320": "GT",
			"316": "GU",
			"624": "GW",
			"328": "GY",
			"344": "HK",
			"340": "HN",
			"191": "HR",
			"332": "HT",
			"348": "HU",
			"360": "ID",
			"372": "IE",
			"376": "IL",
			"833": "IM",
			"356": "IN",
			"86": "IO",
			"368": "IQ",
			"364": "IR",
			"352": "IS",
			"380": "IT",
			"832": "JE",
			"388": "JM",
			"400": "JO",
			"392": "JP",
			"404": "KE",
			"417": "KG",
			"116": "KH",
			"296": "KI",
			"174": "KM",
			"659": "KN",
			"408": "KP",
			"410": "KR",
			"414": "KW",
			"136": "KY",
			"398": "KZ",
			"418": "LA",
			"422": "LB",
			"662": "LC",
			"438": "LI",
			"144": "LK",
			"430": "LR",
			"426": "LS",
			"440": "LT",
			"442": "LU",
			"428": "LV",
			"434": "LY",
			"504": "MA",
			"492": "MC",
			"498": "MD",
			"499": "ME",
			"663": "MF",
			"450": "MG",
			"584": "MH",
			"807": "MK",
			"466": "ML",
			"104": "MM",
			"496": "MN",
			"446": "MO",
			"580": "MP",
			"474": "MQ",
			"478": "MR",
			"500": "MS",
			"470": "MT",
			"480": "MU",
			"462": "MV",
			"454": "MW",
			"484": "MX",
			"458": "MY",
			"508": "MZ",
			"516": "NA",
			"540": "NC",
			"562": "NE",
			"574": "NF",
			"566": "NG",
			"558": "NI",
			"528": "NL",
			"578": "NO",
			"524": "NP",
			"520": "NR",
			"570": "NU",
			"554": "NZ",
			"512": "OM",
			"591": "PA",
			"604": "PE",
			"258": "PF",
			"598": "PG",
			"608": "PH",
			"586": "PK",
			"616": "PL",
			"666": "PM",
			"612": "PN",
			"630": "PR",
			"620": "PT",
			"585": "PW",
			"600": "PY",
			"634": "QA",
			"638": "RE",
			"642": "RO",
			"688": "RS",
			"643": "RU",
			"646": "RW",
			"682": "SA",
			"90": "SB",
			"690": "SC",
			"736": "SD",
			"752": "SE",
			"702": "SG",
			"654": "SH",
			"705": "SI",
			"703": "SK",
			"694": "SL",
			"674": "SM",
			"686": "SN",
			"706": "SO",
			"740": "SR",
			"737": "SS",
			"678": "ST",
			"222": "SV",
			"534": "SX",
			"760": "SY",
			"748": "SZ",
			"796": "TC",
			"148": "TD",
			"260": "TF",
			"768": "TG",
			"764": "TH",
			"762": "TJ",
			"772": "TK",
			"626": "TL",
			"795": "TM",
			"788": "TN",
			"776": "TO",
			"792": "TR",
			"780": "TT",
			"798": "TV",
			"158": "TW",
			"834": "TZ",
			"804": "UA",
			"800": "UG",
			"840": "US",
			"858": "UY",
			"860": "UZ",
			"336": "VA",
			"670": "VC",
			"862": "VE",
			"92": "VG",
			"850": "VI",
			"704": "VN",
			"548": "VU",
			"876": "WF",
			"882": "WS",
			"901": "XEN",
			"902": "XNI",
			"903": "XSC",
			"904": "XWA",
			"887": "YE",
			"710": "ZA",
			"894": "ZM",
			"716": "ZW",
			"-1": "default"}


## teams = ["Наблюдает","В игре"]
def teeMe_handler(info):
	i = 0
	players = []
	condition = int(info[8])*5-5
	while i <= condition:
		try:
			flag = flags[info[i + 12]]
		except:
			flag = "Unknown (%d)" % (i + 12)
			continue
		players.append({"name": info[i + 10],
						"clan": info[i + 11] or "None",
						"flag": flag,
						"score": info[i + 13]})
		i+=5
	if info[9] == info[7]:
		specslots = info[9]
	else:
		specslots = int(info[9]) - (info[7])

	return {"name": info[2],
		   "map": info[3],
		   "type": info[4],
		   "flags": info[5],
		   "player_count_ingame": info[6],
		   "max_players_ingame": info[7],
		   "player_count_spectator": int(info[8]) - int(info[6]),
		   "max_players_spectator": specslots,
		   "max_count_all": info[8],
		   "max_players_all": info[9],
		   "players": players}


def command_chkTeeworldsServer(mType, source, argv):
	answer = u"что?"
	if argv:
		arg = str()
		argv = argv.split()[:3]
		addr, port = str(), 8308
		if len(argv) == 1:
			addr = argv[0]
			if ":" in addr:
				addr, port = addr.split(":")
		elif len(argv) == 2:
			addr, arg =  argv
		else:
			return reply(mType, source, answer)

		port = int(port)
		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.settimeout(30)
			sock.connect((addr, port))
			sock.send("\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x67\x69\x65\x33\x05")
			data = sock.recv(2048)
		except:
			return reply(mType, source, u"Ошибка.")
		if data:
			info = data.split("\x00")
			if info:
				info = teeMe_handler(info)
				if arg == u"игроки":
					players = info["players"]
					if players:
						if mType != "private":
							reply(mType, source, u"В привате.")
							mType = "private"
						answer = u"\n[#] [Ник] [Клан] [Флаг] [Очки]"
						for num, key in enumerate(players, 1):
							answer += "\n{num}. {name} {clan} {flag} {score}".format(num=num, **key)
					else:
						answer = u"Кажется, сервер пустует..."
				else:
					answer = (u"\nСервер: %(name)s\n"
							  u"Карта: %(map)s\n"
							  u"Тип игры: %(type)s\n"
							  u"В игре: %(player_count_ingame)s / %(max_players_ingame)s\n"
							  u"Наблюдающих: %(player_count_spectator)s / %(max_players_spectator)s\n"
							  u"Всего игроков: %(max_count_all)s / %(max_players_all)s.") % info
		else:
			answer = u"Сервер не найден."

		reply(mType, source, answer)

command_handler(command_chkTeeworldsServer, 11, "teeworlds")
