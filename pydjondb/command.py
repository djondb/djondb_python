from defs import *
import network
import cursor
import uuid

class Command:
	def __init__(self):
		self._activeTransactionId = None

	def writeHeader(self, net):
		version = "3.5.60822"
		net.writeString(version)

	def writeOptions(self, net):
		options = {}
		if self._activeTransactionId is not None:
			options["_transactionId"] = self._activeTransactionId;
		net.writeBSON(options)

	def readErrorInformation(self, net):
		resultCode = net.readInt()
		if (resultCode > 0):
			message = net.readString()

	def dropNamespace(self, net, db, ns, transactionId = None):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.DROPNAMESPACE)
		self.writeOptions(net)
		net.writeString(db)
		net.writeString(ns)
		net.flush()

		result = net.readInt()

		self.readErrorInformation(net)
		return True

	def remove(self, net, db, ns, id, revision = None):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.REMOVE)
		self.writeOptions(net)
		net.writeString(db)
		net.writeString(ns)
		net.writeString(id)

		if revision is not None:
			net.writeString(revision)
		else:
			net.writeString("")

		net.flush()

		self.readErrorInformation(net)
		return True

	def showDbs(self, net):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.SHOWDBS)
		self.writeOptions(net)
		net.flush()

		results = net.readInt()
		dbs = []
		for x in range(0, results):
			dbs.append(net.readString())

		self.readErrorInformation(net)
		return dbs

	def showNamespaces(self, net, db):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.SHOWNAMESPACES)
		self.writeOptions(net)
		net.writeString(db)
		net.flush()

		results = net.readInt()
		dbs = []
		for x in range(0, results):
			dbs.append(net.readString())

		self.readErrorInformation(net)
		return dbs

	def insert(self, net, db, ns, data):
		net.reset()
		self.writeHeader(net)
		net.writeInt(0) # Insert command
		self.writeOptions(net)
		net.writeString(db)
		net.writeString(ns)
		net.writeBSON(data)
		net.flush()

		result = net.readInt()
		self.readErrorInformation(net)

	def update(self, net, db, ns, data):
		net.reset()
		self.writeHeader(net)
		net.writeInt(1) # Update command
		self.writeOptions(net)
		net.writeString(db)
		net.writeString(ns)
		net.writeBSON(data)
		net.flush()

		result = net.readInt()
		self.readErrorInformation(net)

	def find(self, net, db, ns, select, filter):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.FIND) # find command
		self.writeOptions(net)
		net.writeString(db)
		net.writeString(ns)
		net.writeString(filter)
		net.writeString(select)
		net.flush()

		cursorId = net.readString()
		flag = net.readInt()
		results = []
		if flag is 1:
			results = net.readBSONArray()

		result = cursor.DjondbCursor(net, cursorId, results)
		self.readErrorInformation(net)
		return result

	def fetchRecords(self, net, cursorId):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.FETCHCURSOR) # find command
		self.writeOptions(net)
		net.writeString(cursorId)
		net.flush()

		flag = net.readInt();
		results = None
		if flag is 1:
			results = net.readBSONArray()
		
		self.readErrorInformation(net)

		return results

	def beginTransaction(self):
		_activeTransactionId = uuid.uuid4()

	def commitTransaction(self):
		if _activeTransactionId is not None:
			net.reset()
			self.writeHeader(net)
			net.writeInt(CommandType.COMMIT) # find command
			self.writeOptions(net)
			net.writeString(_activeTransactionId)
			net.flush()

			self.readErrorInformation(net)
			_activeTransactionId = None
		else:
			raise DjondbException('Nothing to commit, you need beginTransaction before committing or rollback')

	def rollbackTransaction(self):
		if _activeTransactionId is not None:
			net.reset()
			self.writeHeader(net)
			net.writeInt(CommandType.ROLLBACK) # find command
			self.writeOptions(net)
			net.writeString(_activeTransactionId)
			net.flush()

			self.readErrorInformation(net)
			_activeTransactionId = None
		else:
			raise DjondbException('Nothing to rollback, you need beginTransaction before committing or rollback')

	def createIndex(self, indexDef):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.CREATEINDEX) # createindex command
		self.writeOptions(net)
		net.writeBSON(indexDef)
		net.flush()

		self.readErrorInformation(net)

	def backup(self, db, destFile):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.BACKUP) # createindex command
		self.writeOptions(net)
		self.writeString(db)
		self.writeString(destFile)
		net.flush()

		result =  self.readInt()
		self.readErrorInformation(net)
		return result



