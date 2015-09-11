# BS mark.1-55
# coding: utf-8

#  BlackSmith plugin
#  Interpreter Plugin
#  Idea (c) Unknown Author
#  Code (c) simpleApps, 2011

def pyEval(mType, source, code):
	try: result = unicode(eval(code))
	except Exception: result = returnExc()
	if not result:
		result = `result`
	reply(mType, source, result)

def pyExec(mType, source, code):
	result = u"Done."
	try: exec(unicode(code + "\n"), globals())
	except Exception: result = returnExc()
	reply(mType, source, result)

## PyShell is a name of one our project...
def pyShell(mType, source, cmd):
	if os.name == "posix":
		cmd = "sh -c \"%s\" 2>&1" % (cmd.encode("utf-8"))
	elif os.name == "nt":
		cmd = cmd.encode("cp1251")
	shell = os.popen(cmd)
	result = shell.read()
	if os.name == "nt": result = result.decode("cp866")
	if not result: result = "Done."
	reply(mType, source, result)

calcExp = re.compile("([0-9]|[\+\-\(\/\*\)\%\^\.\ ])")
def pyCalc(mType, source, expression):
	if expression and len(expression) < 40 and not expression.count("**"):
		if calcExp.sub("", expression):
			result = "Недопустимо."
		else:
			try:
				result = eval(expression)
			except ZeroDivisionError:
				result = unichr(8734)
			except Exception:
				result = "An exception found."
	else:
		result = `None`
	reply(mType, source, str(result))

command_handler(pyEval, 100, "interpreter")
command_handler(pyExec, 100, "interpreter")
command_handler(pyShell, 100, "interpreter")
command_handler(pyCalc, 10, "interpreter")