class CommandType:
	INSERT = 0
	UPDATE = 1
	FIND = 2
	CLOSECONNECTION = 3
	DROPNAMESPACE = 4
	SHUTDOWN = 5
	SHOWDBS = 6
	SHOWNAMESPACES = 7
	REMOVE = 8
	COMMIT = 9
	ROLLBACK = 10
	FETCHCURSOR = 11
	FLUSHBUFFER = 12
	CREATEINDEX = 13
	BACKUP = 14
	RCURSOR = 15
	PERSISTINDEXES = 16
	EXECUTEQUERY = 17
	EXECUTEUPDATE = 18

class DjondbException(Exception):
	def __init__(self, code, message):
		self.code = code
		self.message = message
	def __str__(self):
		return "Exception Code: %d. Message: %s" % (self.code, self.message)

