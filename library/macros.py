#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Talisman module
#  macros.py

# Author:
#  dimichxp [dimichxp@gmail.com]
# Modifications:
#  Als [Als@exploit.in]
#  WitcherGeralt [WitcherGeralt@rocketmail.com]

import random, re, os

def shell_esc(_shell_):
	for symbol in [';', '&', '|', '`', '$', '\\', '#']:
		_shell_ = _shell_.replace(symbol, '')
	return _shell_

def xml_esc(_xml_):
	list = {'\'': '&apos;', '>': '&gt;', '<': '&lt;', '&': '&amp;', '\"': '&quot;'}
	for symbol in list:
		_xml_ = _xml_.replace(symbol, list[symbol])
	return _xml_

from enconf import *

def macro_get_rand(mass, source):
	try:
		num1 = int(mass[0])
		num2 = int(mass[1])
		number = random.randrange(num1, num2)
	except:
		number = 12
	return str(number)

def macro_shell_escape(mass, source):
	return shell_esc(mass[0])

def macro_xml_escape(mass, source):
	return xml_esc(mass[0])

def macro_context(mass, source):
	item, esc = mass[0], ''
	if item == 'conf':
		esc = xml_esc(source[1])
	elif item == 'nick':
		esc = xml_esc(source[2])
	elif item == 'conf_jid':
		esc = xml_esc(source[0])
	return esc

class MacroCommands:
	commands = {'rand': [2, macro_get_rand], 'shell_escape': [1, macro_shell_escape], 'xml_escape': [1, macro_xml_escape], 'context': [1, macro_context]}

	def map_char(self, x, i):
		st = i['state']
		if i['esc']:
			i['esc'] = False
			ret = i['level']
		elif x == '\\':
			i['esc'] = True
			ret = 0
		elif x == '%':
			i['state'] = 'cmd_p'
			ret = 0
		elif x == '(':
			if i['state'] == 'cmd_p':
				i['level'] += 1
				i['state'] = 'args'
			ret = 0
		elif x == ')':
			if i['state'] == 'args':
				i['state'] = 'null'
			ret = 0
		else:
			if i['state'] == 'args':
				ret = i['level']
			else:
				i['state'] = 'null'
				ret = 0
		return ret

	def get_map(self, inp):
		i = {'level': 0, 'state': 'null', 'esc': False}
		return [self.map_char(x, i) for x in list(inp)]

	def parse_cmd(self, me):
		i = 0
		m = self.get_map(me)
		fk = [''] * max(m)
		while i < len(m):
			if m[i] != 0:
				fk[m[i]-1] += me[i]
			i += 1
		return fk

	def execute_cmd(self, cmd, fk, source):
		print cmd, fk
		if self.commands.has_key(cmd):
			if self.commands[cmd][0] <= len(fk):
				return self.commands[cmd][1](fk, source)
		return ''

	def proccess(self, cmd, source):
		command = cmd[0]
		fk = cmd[1:]
		return self.execute_cmd(command, fk, source)

def read_file(filename):
	filename = chkFile(filename)
	try:
		fl = file(filename, 'r')
		data = fl.read()
		fl.close()
	except:
		data = "{}"
	return data

def write_file(filename, data):
	filename = chkFile(filename)
	try:
		fl = file(filename, 'w')
		fl.write(data)
		fl.close()
	except:
		pass

class Macros:
	gmacrolist = {}
	gaccesslist = {}
	macrolist = {}
	accesslist = {}
	macrocmds = MacroCommands()

	def init(self):
		try:
			self.gmacrolist = eval(read_file('dynamic/macros.txt'))
		except:
			self.gmacrolist = {}
		try:
			self.gaccesslist = eval(read_file('dynamic/macroaccess.txt'))
		except:
			self.gaccesslist = {}

	def load(self, conf):
		try:
			self.macrolist[conf] = eval(read_file('dynamic/'+conf+'/macros.txt'))
		except:
			self.macrolist[conf] = {}
		try:
			self.accesslist[conf] = eval(read_file('dynamic/'+conf+'/macroaccess.txt'))
		except:
			self.accesslist[conf] = {}

	def flush(self, conf = None, act = 'all'):
		if conf:
			if act in ['macr', 'all']:
				write_file('dynamic/'+conf+'/macros.txt', str(self.macrolist[conf]))
			if act in ['sacc', 'all']:
				write_file('dynamic/'+conf+'/macroaccess.txt', str(self.accesslist[conf]))
		else:
			if act in ['macr', 'all']:
				write_file('dynamic/macros.txt', str(self.gmacrolist))
			if act in ['sacc', 'all']:
				write_file('dynamic/macroaccess.txt', str(self.gaccesslist))

	def add(self, mapee, map, conf = None):
		if conf:
			if not self.macrolist.has_key(conf):
				self.macrolist[conf] = {}
			self.macrolist[conf][mapee] = map
		else:
			self.gmacrolist[mapee] = map

	def remove(self, mapee, conf = None):
		if conf:
			if self.macrolist[conf].has_key(mapee):
				del self.macrolist[conf][mapee]
			if self.accesslist[conf].has_key(mapee):
				del self.accesslist[conf][mapee]
		else:
			if self.gmacrolist.has_key(mapee):
				del self.gmacrolist[mapee]
			if self.gaccesslist.has_key(mapee):
				del self.gaccesslist[mapee]

	def map_char(self, x, i):
		ret = i['level']
		if i['esc']:
			i['esc'] = False
		elif x == '\\':
			i['esc'] = True
			ret = 0
		elif x == '`':
			i['larg'] = not i['larg']
			ret = 0
		elif x == ' ':
			if not i['larg']:
				i['level'] += 1
				ret = 0
		return ret

	def get_map(self, inp):
		i = {'larg': False, 'level': 1, 'esc': False}
		return [self.map_char(x, i) for x in list(inp)]

	def parse_cmd(self, me):
		i = 0
		m = self.get_map(me)
		fk = [''] * max(m)
		while i < len(m):
			if m[i] != 0:
				fk[m[i]-1] += me[i]
			i += 1
		return fk

	def expand(self, cmd, source):
		if not cmd:
			return ""
		cl = self.parse_cmd(cmd)
		if not cl:
			return cmd
		command = cl[0].split()
		if command:
			command = command[0].lower()
		else:
			return
		fk, exp = cl[1:], ''
		if self.macrolist.has_key(source[1]):
			for macro in self.macrolist[source[1]]:
				try:
					if len(command) <= len(macro) and command == macro[0: len(macro)]:
						if self.macrolist[source[1]][macro]:
							exp = self.apply(self.macrolist[source[1]][macro], fk, source)
				except:
					pass
		for macro in self.gmacrolist:
			try:
				if len(command) <= len(macro) and command == macro[0: len(macro)]:
					if self.gmacrolist[macro]:
						exp = self.apply(self.gmacrolist[macro], fk, source)
			except:
				pass
		if not exp:
			return cmd
		rexp = self.expand(exp, source)
		return rexp

	def comexp(self, cmd, source, key = ''):
		if not cmd:
			return ""
		cl = self.parse_cmd(cmd)
		if not cl:
			return cmd
		command = cl[0].split(' ')[0]
		fk, exp = cl[1:], ''
		if self.macrolist.has_key(source[1]):
			for macro in self.macrolist[source[1]]:
				try:
					if len(command) <= len(macro) and command == macro[0: len(macro)]:
						if self.macrolist[source[1]][macro]:
							exp = self.apply(self.macrolist[source[1]][macro], fk, source)
				except:
					pass
		for macro in self.gmacrolist:
			try:
				if len(command) <= len(macro) and command == macro[0: len(macro)]:
					if self.gmacrolist[macro]:
						exp = self.apply(self.gmacrolist[macro], fk, source)
			except:
				pass
		if not exp:
			return cmd
		rexp = self.comexp(exp, source, key)
		return rexp

	def apply(self, macro, fk, source):
		m = self.macrocmds.parse_cmd(macro)
		expanded = macro.replace('$*', ' '.join(fk))
		for i in m:
			cmd = [x.strip() for x in i.split(',')]
			for j in re.findall('\$[0-9]+', i):
				index = int(j[1:]) - 1
				if len(fk) <= index:
					return expanded
				cmd = [x.replace(j, fk[index]) for x in cmd]
			res = self.macrocmds.proccess(cmd, source)
			if res:
				expanded = expanded.replace('%('+i+')', res)
		for j in re.findall('\$[0-9]+', expanded):
			index = int(j[1:]) - 1
			if len(fk) <= index:
				return expanded
			expanded = expanded.replace(j, fk[index])
		return expanded

	def get_access(self, macro, conf):
		if self.macrolist.has_key(conf):
			if self.accesslist[conf].has_key(macro):
				return self.accesslist[conf][macro]
		if self.gaccesslist.has_key(macro):
			return self.gaccesslist[macro]
		return -5

	def give_access(self, macro, access, conf = None):
		if conf:
			if conf not in self.accesslist:
				self.accesslist[conf] = {}
			self.accesslist[conf][macro] = access
		else:
			self.gaccesslist[macro] = access
