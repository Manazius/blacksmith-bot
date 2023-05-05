# /* coding: utf-8 */
# Conference Encoder.
# © WitcherGeralt, modifications by simpleApps

from string import digits
from string import ascii_letters


__exceptions = "-/.@_"
ascii_tab = tuple(digits + ascii_letters + __exceptions)

def chkFile(filename):
	filename = filename.replace("\t", "\\t")
	filename = filename.replace("\n", "\\n")
	filename = filename.replace("\r", "\\r")
	if filename.count("/") > 1:
		if not chkUnicode(filename):
			filename = nameEncode(filename)
	return filename

def chkUnicode(body, tab = ascii_tab):
	if tab != ascii_tab:
		tab = tuple(tab)
		tab += ascii_tab
	for symbol in body:
		if symbol not in tab:
			return False
	return True

def nameEncode(path):
	encodedName = list()
	from base64 import b16encode
	for Name in path.split(chr(47)):
		At = chr(64)
		if Name.count(At):
			List = Name.split(At, 1)
			chatName = b16encode(List[0].encode("utf-8"))
			encodedName.append("%s@%s" % (chatName[(len(chatName) / 2):], List[1]))
		else:
			encodedName.append(Name)
	del b16encode
	return chr(47).join(encodedName)

del digits, ascii_letters, __exceptions