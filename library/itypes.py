"""
'itypes' module by WitcherGeralt (alkorgun@gmail.com)

Module contains Classes with Superstructure.
It's just for convenience.
"""

import sqlite3

__all__ = [
	"Number",
	"Database"
				]

__version__ = "0.6"

class Number(object):

	def __init__(self, number = int()):
		self.iter = number

	def plus(self, number = 0x1):
		self.__init__(self.iter + number)
		return int(self.iter)

	def reduce(self, number = 0x1):
		self.__init__(self.iter - number)
		return int(self.iter)

	__int__ = lambda self: self.iter.__int__()

	_int = lambda self: self.__int__()

	__str__ = lambda self: self.iter.__str__()

	_str = lambda self: self.__str__()

	__float__ = lambda self: self.iter.__float__()

	__repr__ = lambda self: self.iter.__repr__()

class Database:

	def __init__(self, filename, timeout = 8):
		self.db = sqlite3.connect(filename, timeout = timeout)
		self.cursor = self.db.cursor()
		self.commit = self.db.commit
		self.execute = self.cursor.execute
		self.filename = filename
		self.__call__ = self.execute
		self.fetchone = self.cursor.fetchone
		self.fetchall = self.cursor.fetchall
		self.fetchmany = self.cursor.fetchmany

	def close(self):
		if self.cursor:
			self.cursor.close()
		if self.db.total_changes:
			self.commit()
		if self.db:
			self.db.close()

	def __enter__(self):
		return self

	def __exit__(self, *ls):
		self.close()
