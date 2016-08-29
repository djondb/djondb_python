from defs import *
import command

class CursorStatus:
	CS_LOADING = 1
	CS_RECORDS_LOADED = 2
	CS_CLOSED = 3

class DjondbCursor:
	def __init__(self, net, cursorId=None, firstPage=None):
		self._net = net
		self._cursorId = cursorId
		self._rows = firstPage
		self._position = 0
		self._current = None

		if self._rows is None:
			self._count = 0
		else:
			self._count = len(self._rows)

		if cursorId is not None:
			self._status = CursorStatus.CS_LOADING
		else:
			self._status = CursorStatus.CS_RECORDS_LOADED

	def next(self):
		if self._status == CursorStatus.CS_CLOSED:
			raise DjondbException('Cursor is closed')
		result = True
		if self._count > self._position:
			self._current = self._rows[self._position]
			self._position += 1
		else:
			if self._status is CursorStatus.CS_LOADING:
				page = command.Command().fetchRecords(self._net, self._cursorId)
				if page is None:
					self._status = CursorStatus.CS_RECORDS_LOADED
					result = False
				else:
					self._rows.extend(page)
					self._count = len(self._rows)
					result = self.next()
			else:
				result = false;

		return result

	def previous(self):
		if self._status == CursorStatus.CS_CLOSED:
			raise DjondbException('Cursor is closed')
		result = True
		if self._count > 0 and self._position > 0:
			self._position -= 1
			self._current = self._rows[self._position]
		else:
			result = False
		return result

	def current(self):
		return self._current
