# BS mark.1-55
# /* coding: utf-8 */

#  BlackSmith mark.1
#  quiz.py

# (c) Gigabyte
# http://jabbrik.ru

#-extmanager-depends:static/questions.txt-#
#-extmanager-extVer:2.0-# 


QUIZ_FILE = 'static/questions.txt'
QUIZ_TOTAL_LINES = 10240
QUIZ_TIME_LIMIT = 200
QUIZ_IDLE_LIMIT = 3
QUIZ_RECURSIVE_MAX = 20
QUIZ_CURRENT_ANSWER = {}
QUIZ_QUESTION = {}
QUIZ_CURRENT_HINT = {}
QUIZ_CURRENT_HINT_NEW = {}
QUIZ_CURRENT_TIME = {}
QUIZ_IDLENESS = {}
QUIZ_IDLE_ANSWER = {}
QUIZ_START = {}
QUIZ_IDLE_ANSWER_FIRSR = {}
QUIZ_NOWORD = '*'
MODE = 'M1'
PTS = 'P2'
ACC = 'A2'

HELP = u'помощь по командам > "викторина"'

def sectomin(time):
	m = 0
	s = 0
	if time >= 60:
		m = time / 60
		if (m * 60) != 0:
			s = time - (m * 60)
		else:
			s = 0
	else:
		m = 0
		s = time
	return str(m)+u'мин. и '+str(s)+u'сек.'

def quiz_timer(conf, start_time):
	time.sleep(QUIZ_TIME_LIMIT)
	if conf in QUIZ_CURRENT_TIME and conf in QUIZ_CURRENT_ANSWER and start_time == QUIZ_CURRENT_TIME[conf]:
		QUIZ_CURRENT_ANSWER[conf]
		msg(conf, u'(!) Время вышло! '+sectomin(QUIZ_TIME_LIMIT)+u' прошло. Правильный ответ: '+QUIZ_CURRENT_ANSWER[conf])
		if conf in QUIZ_IDLENESS:
			QUIZ_IDLENESS[conf] += 1
		else:
			QUIZ_IDLENESS[conf] = 1
		if QUIZ_IDLENESS[conf] >= QUIZ_IDLE_LIMIT:
			msg(conf, u'(!) Викторина автоматичеки заверщена по бездействию! '+str(QUIZ_IDLE_LIMIT)+' вопросов без ответа.')
			del QUIZ_CURRENT_ANSWER[conf]
			quiz_list_scores(conf)
		else:
			quiz_ask_question(conf)

def quiz_new_question():
	line_num = random.randrange(QUIZ_TOTAL_LINES)
	fl = file(QUIZ_FILE)
	for n in range(line_num + 1):
		if n == line_num:
			(question, answer) = fl.readline().strip().split('|', 1)
			return (unicode(question, 'utf-8'), unicode(answer, 'utf-8'))
		else:
			fl.readline()

def quiz_ask_question(conf):
	globals()['QUIZ_IDLE_ANSWER'] = {conf: {}}
	(question, answer) = quiz_new_question()
	QUIZ_QUESTION[conf] = question
	QUIZ_CURRENT_ANSWER[conf] = answer
	QUIZ_CURRENT_HINT[conf] = None
	QUIZ_CURRENT_HINT_NEW[conf] = None
	QUIZ_CURRENT_TIME[conf] = time.time()
	INFO['thr'] += 1
	try:
		threading.Thread(None, quiz_timer,'quiz-'+str(INFO['thr']),(conf, QUIZ_CURRENT_TIME[conf])).start()
	except:
		LAST['null'] += 1
	msg(conf, u'(?) Внимание вопрос: \n'+question)

def quiz_ask_new_question(conf, ans):
	globals()['QUIZ_IDLE_ANSWER'] = {conf: {}}
	(question, answer) = quiz_new_question()
	QUIZ_QUESTION[conf] = question
	QUIZ_CURRENT_ANSWER[conf] = answer
	QUIZ_CURRENT_HINT[conf] = None
	QUIZ_CURRENT_HINT_NEW[conf] = None
	QUIZ_CURRENT_TIME[conf] = time.time()
	INFO['thr'] += 1
	try:
		threading.Thread(None, quiz_timer,'quiz-'+str(INFO['thr']),(conf, QUIZ_CURRENT_TIME[conf])).start()
	except:
		LAST['null'] += 1
	msg(conf, u'(!) Правильный ответ: '+ans+u', cмена вопроса: \n'+question)

def quiz_answer_question(conf, nick, answer):
	BASE = 'dynamic/'+conf+'/quiz.cfg'
	QUIZ_SCORES = eval(read_file(BASE))
	if conf in QUIZ_CURRENT_ANSWER:
		jid = handler_jid(conf+'/'+nick)
		answer1 = QUIZ_CURRENT_ANSWER[conf].lower()
		answer2 = answer.lower()
		if answer1 == answer2:
			if conf in QUIZ_IDLE_ANSWER:
				if len(QUIZ_IDLE_ANSWER[conf]) != 0:
					if jid in QUIZ_IDLE_ANSWER[conf]:
						if QUIZ_IDLE_ANSWER[conf][jid][1] == '1':
							msg(conf, nick+u': Ты уже ответил верно!')
						else:
							razn = QUIZ_IDLE_ANSWER[conf][jid][0] - QUIZ_IDLE_ANSWER_FIRSR[conf]
							msg(conf, nick+u': Ты уже ответил правильно, опоздав на %.3f сек' % razn)
					else:
						QUIZ_IDLE_ANSWER[conf][jid] = [time.time(), '0']
						razn = QUIZ_IDLE_ANSWER[conf][jid][0] - QUIZ_IDLE_ANSWER_FIRSR[conf]
						msg(conf, nick+u': Ты ответил правильно, но опоздал на %.3f сек' % razn)
					return
			if conf in QUIZ_IDLENESS:
				del QUIZ_IDLENESS[conf]
			answer_time = int(time.time() - QUIZ_CURRENT_TIME[conf])
			try:
				if MODE == 'M1':
					alen = len(QUIZ_CURRENT_HINT_NEW[conf])
					blen = QUIZ_CURRENT_HINT_NEW[conf].count('')
					a = alen - blen
				if MODE == 'M2':
					a = 0
					a = a + QUIZ_CURRENT_HINT[conf]
			except:
				a = 1
			if PTS == 'P1':
				points = QUIZ_TIME_LIMIT / answer_time / 3 + 1 / a
			if PTS == 'P2':
				try:
					alen = len(QUIZ_CURRENT_HINT_NEW[conf])
					blen = QUIZ_CURRENT_HINT_NEW[conf].count('')
					a = alen - blen
					procent = a * 100 / alen
				except:
					procent = 10
				points = (QUIZ_TIME_LIMIT / answer_time) / (procent / 10)
			if points == 0:
				pts = '0'
			else:
				pts = '+'+str(points)
			msg(conf, u'(!) '+nick+u', поздравляю! Лови '+pts+u' очка в банк! Верный ответ: '+answer)
			if conf not in QUIZ_SCORES:
				QUIZ_SCORES[conf] = {}
			if jid in QUIZ_SCORES[conf]:
				QUIZ_SCORES[conf][jid][0] += points
				QUIZ_SCORES[conf][jid][1] += points
				QUIZ_SCORES[conf][jid][2] = nick
				QUIZ_SCORES[conf][jid][3] += 1
			else:
				QUIZ_SCORES[conf][jid] = [points, points, nick, 1]
			if conf not in QUIZ_IDLE_ANSWER:
				QUIZ_IDLE_ANSWER[conf] = {}
			QUIZ_IDLE_ANSWER[conf][jid] = [time.time(), '1']
			QUIZ_IDLE_ANSWER_FIRSR[conf] = time.time()
			if len(QUIZ_IDLE_ANSWER[conf]) == 1:
				time.sleep(1.0)
				quiz_ask_question(conf)
		write_file(BASE, str(QUIZ_SCORES))

def swap(arr, i, j):
	arr[i], arr[j] = arr[j], arr[i]

def sort(conf, mas, sort = 1, count = 10):
	base = mas[conf]
	arr = []
	str1 = ''
	for a in base:
		asd = base[a][sort]
		arr += [asd]
	i = len(arr)
	while i > 1:
		for j in xrange(i - 1):
			if arr[j] < arr[j + 1]:
				swap(arr, j, j + 1)
		i -= 1
	top10 = 1
	prim = ''
	charcount = 0
	for z in arr:
		for x in base:
			nick = base[x][2]
			if len(nick) > charcount:
				charcount = len(nick)
	for z in arr:
		for x in base:
			nick = base[x][2]
			if len(nick) < charcount:
				nick += ' ' * (charcount - len(nick))
			nick += ' '
			if base[x][sort] == z:
				str1 += str(top10)+'. '+nick+' '+str(base[x][0])+'-'+str(base[x][1])+'-'+str(base[x][3])+'\n'
				if top10 < count:
					top10 += 1
				else:
					str1 = prim+str1
					return str1
	str1 = prim+str1
	return str1

def quiz_list_scores(conf, sort_ = 1, count = 10):
	BASE = 'dynamic/'+conf+'/quiz.cfg'
	QUIZ_SCORES = eval(read_file(BASE))
	if conf in QUIZ_SCORES:
		if QUIZ_SCORES[conf]:
			if conf in QUIZ_IDLENESS:
				del QUIZ_IDLENESS[conf]
			if conf in QUIZ_CURRENT_ANSWER:
				result = u'(*) Текущий счет:\n[Ник][Счет за игру][Общий счет][Кол-во ответов]\n'
			else:
				result = u'(*) Текущий счет:\n[Ник][Последний счет][Общий счет][Кол-во ответов]\n'
			result = result+sort(conf, QUIZ_SCORES, sort_, count)
			msg(conf, result)

def handler_quiz_start(type, source, body):
	if source[1] in GROUPCHATS:
		if source[1] not in QUIZ_CURRENT_ANSWER:
			BASE = 'dynamic/'+source[1]+'/quiz.cfg'
			QUIZ_SCORES = eval(read_file(BASE))
			if source[1] not in QUIZ_SCORES:
				QUIZ_SCORES[source[1]] = {}
				write_file(BASE, str(QUIZ_SCORES))
			jid = handler_jid(source[0])
			if source[1] in QUIZ_SCORES:
				if jid in QUIZ_SCORES[source[1]]:
					for kjid in QUIZ_SCORES[source[1]]:
						QUIZ_SCORES[source[1]][kjid][0] = 0
					write_file(BASE, str(QUIZ_SCORES))
			QUIZ_START[source[1]] = jid
			if source[1] in QUIZ_IDLENESS:
				del QUIZ_IDLENESS[source[1]]
			quiz_ask_question(source[1])
		else:
			reply(type, source, u'Викторина- уже существует! '+HELP)
	else:
		reply(type, source, u'только в чате')

def handler_quiz_stop(type, source, body):
	if source[1] in QUIZ_CURRENT_ANSWER:
		del QUIZ_CURRENT_ANSWER[source[1]]
		msg(source[1], u'(!) Викторина остановлена.')
		time.sleep(1.0)
		quiz_list_scores(source[1], 0, 10)
	else:
		reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_next(type, source, body):
	if source[1] in QUIZ_CURRENT_ANSWER:
		if ACC == 'A1':
			quiz_ask_new_question(source[1], QUIZ_CURRENT_ANSWER[source[1]])
		if ACC == 'A2':
			jid = handler_jid(source[0])
			if (jid == QUIZ_START[source[1]]) | (user_level(source[0], source[1]) >= 16):
				quiz_ask_new_question(source[1], QUIZ_CURRENT_ANSWER[source[1]])
			else:
				reply(type, source, u'Настройкой плагина запрещено пользование этой командой членам, '+HELP)
	else:
		reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_hint(type, source, body):
	if source[1] in QUIZ_CURRENT_ANSWER:
		globals()['ans'] = QUIZ_CURRENT_ANSWER[source[1]]
		if source[1] in QUIZ_IDLENESS:
			del QUIZ_IDLENESS[source[1]]
		if QUIZ_CURRENT_HINT[source[1]] == None:
			QUIZ_CURRENT_HINT[source[1]] = 0
		if MODE == 'M1':
			if QUIZ_CURRENT_HINT_NEW[source[1]] == None:
				ms = ['']
				QUIZ_CURRENT_HINT_NEW[source[1]] = []
				for r in range(0, len(QUIZ_CURRENT_ANSWER[source[1]])):
					QUIZ_CURRENT_HINT_NEW[source[1]] += ms
			ex = 1
			while ex == 1:
				a = random.choice(QUIZ_CURRENT_ANSWER[source[1]])
				if not a in QUIZ_CURRENT_HINT_NEW[source[1]]:
					for t in range(0, len(QUIZ_CURRENT_ANSWER[source[1]])):
						if QUIZ_CURRENT_ANSWER[source[1]][t] == a:
							QUIZ_CURRENT_HINT_NEW[source[1]][t] = a
							ex = 0
				hint = ''
			for hnt in QUIZ_CURRENT_HINT_NEW[source[1]]:
				if hnt == '':
					hint += QUIZ_NOWORD
				else:
					hint += hnt
			if not '' in QUIZ_CURRENT_HINT_NEW[source[1]]:
				quiz_ask_new_question(source[1], globals()['ans'])
			else:
				msg(source[1], u'(*) Подсказка: '+hint)
		if MODE == 'M2':
			QUIZ_CURRENT_HINT[source[1]] += 1
			hint = QUIZ_CURRENT_ANSWER[source[1]][0: QUIZ_CURRENT_HINT[source[1]]]
			hint += ' *' * (len(QUIZ_CURRENT_ANSWER[source[1]]) - QUIZ_CURRENT_HINT[source[1]])
			msg(source[1], u'(*) Подсказка: '+hint)
			if (len(QUIZ_CURRENT_ANSWER[source[1]]) - QUIZ_CURRENT_HINT[source[1]]) == 0:
				quiz_ask_new_question(source[1], globals()['ans'])
	else:
		reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_answer(type, source, body):
	if source[1] in QUIZ_CURRENT_ANSWER:
		reply(type, source, QUIZ_CURRENT_ANSWER[source[1]])
	else:
		reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_scores(type, source, body):
	if source[1] in GROUPCHATS:
		BASE = 'dynamic/'+source[1]+'/quiz.cfg'
		QUIZ_SCORES = eval(read_file(BASE))
		if source[1] in  QUIZ_SCORES:
			if QUIZ_SCORES[source[1]]:
				if source[1] in QUIZ_CURRENT_ANSWER:
					quiz_list_scores(source[1], 0, 10)
				else:
					quiz_list_scores(source[1], 1, 10)
			else:
				reply(type, source, u'В БД пусто, '+HELP)
		else:
			reply(type, source, u'В БД пусто, '+HELP)
	else:
		reply(type, source, u'только в чате')

def handler_quiz_message(raw, type, source, body):
	if source[1] in QUIZ_CURRENT_ANSWER:
		quiz_answer_question(source[1], source[2], body.strip())

def handler_quiz_resend(type, source, body):
	if source[1] in QUIZ_QUESTION:
		reply(type, source, u'(*) Текущий вопрос:\n'+QUIZ_QUESTION[source[1]])
	else:
		reply(type, source, u'Нет викторины, '+HELP)

def handler_quiz_help(type, source, body):
	if source[1] in QUIZ_CURRENT_ANSWER:
		stat = u'запущена'
	else:
		stat = u'не запущена'
	res = u'Сейчас викторина: '+stat+u'\nВ базе данных: '+str(QUIZ_TOTAL_LINES)+u' вопросов\nКоманды:\n- игра - запуск игры\n- стой - остановка игры\n- повтори - повторяет вопрос\n- помоги - вывод подсказки (снимает баллы)\n- дальше - следущий вопрос\n- счет - вывод текущего счета и мини статистика\n- избазы - удаление всей статистики для комнаты (без параметра), или для юзера (жид в параметре)\n+ сортировка статистики (во время игры по текущему счету, при окончании игры по текущему счету, вне игры по общему счету)\n+ форматирование статистики\n+ очистка статистики'
	if MODE == 'M1':
		m = u'* Новый тип хинтов (рандомный)'
	if MODE == 'M2':
		m = u'* Старый тип хинтов'
	if PTS == 'P1':
		p = u'* Старый тип начисления очков'
	if PTS == 'P2':
		p = u'* Новый тип начисления очков'
	if ACC == 'A1':
		a = u'* Доступ к !сл имеют все'
	if ACC == 'A2':
		a = u'* Доступ к !сл имеет только тот кто создал викторину и модераторы'
	res += u'\nКонфигурация:\n'+m+'\n'+p+'\n'+a
	reply(type, source, res)

def handler_quiz_base_del(type, source, body):
	if source[1] in GROUPCHATS:
		BASE = 'dynamic/'+source[1]+'/quiz.cfg'
		QUIZ_SCORES = eval(read_file(BASE))
		if body == '':
			if source[1] in QUIZ_SCORES:
				del QUIZ_SCORES[source[1]]
				reply(type, source, u'<!> База данных была полностью очищена!')
			else:
				reply(type, source, u'<!> База данных и так пустая!')
		elif source[1] in QUIZ_SCORES:
			if body in QUIZ_SCORES[source[1]]:
				del QUIZ_SCORES[source[1]][body]
				reply(type, source, u'<!> Данные на указаный жид удалены')
			else:
				reply(type, source, u'<!> База данных и так пустая!')
		else:
			reply(type, source, u'<!> База данных была полностью очищена!')
		write_file(BASE, str(QUIZ_SCORES))
	else:
		reply(type, source, u'только в чате')

def quiz_file_init(conf):
	if not check_file(conf, 'quiz.cfg'):
		delivery(u'Внимание! Не удалось создать quiz.cfg для "%s"!' % (conf))

handler_register("01eh", handler_quiz_message)

command_handler(handler_quiz_help, 10, "quiz")
command_handler(handler_quiz_answer, 80, "quiz")
command_handler(handler_quiz_base_del, 100, "quiz")
command_handler(handler_quiz_start, 10, "quiz")
command_handler(handler_quiz_resend, 10, "quiz")
command_handler(handler_quiz_stop, 10, "quiz")
command_handler(handler_quiz_hint, 10, "quiz")
command_handler(handler_quiz_scores, 10, "quiz")
command_handler(handler_quiz_next, 10, "quiz")

handler_register("01si", quiz_file_init)
