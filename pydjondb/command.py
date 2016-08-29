from defs import *
import network
import cursor
import uuid
import datetime

class Command:
	def __init__(self):
		self._activeTransactionId = None
		self.resultCode = 0
		self.resultMessage = None

	def writeHeader(self, net):
		version = "3.5.60822"
		net.writeString(version)

	def writeOptions(self, net):
		options = {}
		if self._activeTransactionId is not None:
			options["_transactionId"] = self._activeTransactionId;
		net.writeBSON(options)

	def readErrorInformation(self, net):
		self.resultCode = net.readInt()
		if (self.resultCode > 0):
			self.resultMessage = net.readString()

	def readResultDropNamespace(self, net):
		result = net.readInt()

		self.readErrorInformation(net)
		return True

	def dropNamespace(self, net, db, ns, transactionId = None):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.DROPNAMESPACE)
		self.writeOptions(net)
		net.writeString(db)
		net.writeString(ns)
		net.flush()
		return self.readResultDropNamespace(net)

	def readResultRemove(self, net):
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
		return self.readResultRemove(net)

	def readResultShowDbs(self, net):
		results = net.readInt()
		dbs = []
		for x in range(0, results):
			dbs.append(net.readString())

		self.readErrorInformation(net)
		return dbs

	def showDbs(self, net):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.SHOWDBS)
		self.writeOptions(net)
		net.flush()
		return self.readResultShowDbs(net)


	def readResultShowNamespaces(self, net):
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
		return self.readResultShowNamespaces(net)


	def readResultInsert(self, net):
		result = net.readInt()
		self.readErrorInformation(net)

	def insert(self, net, db, ns, data):
		net.reset()
		self.writeHeader(net)
		net.writeInt(0) # Insert command
		self.writeOptions(net)
		net.writeString(db)
		net.writeString(ns)
		net.writeBSON(data)
		net.flush()
		self.readResultInsert(net)


	def readResultUpdate(self, net):
		result = net.readBoolean()
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
		self.readResultUpdate(net)

	def readResultFind(self, net):
		cursorId = net.readString()
		flag = net.readInt()
		results = []
		if flag is 1:
			results = net.readBSONArray()

		result = cursor.DjondbCursor(net, cursorId, results)
		self.readErrorInformation(net)
		return result

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
		return self.readResultFind(net)

	def readResultFetchRecords(self, net):
		flag = net.readInt();
		results = None
		if flag is 1:
			results = net.readBSONArray()
		
		self.readErrorInformation(net)

		return results

	def fetchRecords(self, net, cursorId):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.FETCHCURSOR) # find command
		self.writeOptions(net)
		net.writeString(cursorId)
		net.flush()
		return self.readResultFetchRecords(net)

	def beginTransaction(self):
		self._activeTransactionId = str(uuid.uuid4())

	def readResultCommitTransaction(self, net):
		self.readErrorInformation(net)

	def commitTransaction(self, net):
		if self._activeTransactionId is not None:
			net.reset()
			self.writeHeader(net)
			net.writeInt(CommandType.COMMIT) # find command
			self.writeOptions(net)
			net.writeString(self._activeTransactionId)
			net.flush()

			self.readResultCommitTransaction(net)
			self._activeTransactionId = None
		else:
			raise DjondbException(10001, 'Nothing to commit, you need beginTransaction before committing or rollback')

	def readResultRollbackTransaction(self, net):
		self.readErrorInformation(net)

	def rollbackTransaction(self, net):
		if self._activeTransactionId is not None:
			net.reset()
			self.writeHeader(net)
			net.writeInt(CommandType.ROLLBACK) # find command
			self.writeOptions(net)
			net.writeString(self._activeTransactionId)
			net.flush()

			self.readResultRollbackTransaction(net)
			self._activeTransactionId = None
		else:
			raise DjondbException(10001, 'Nothing to rollback, you need beginTransaction before committing or rollback')

	def readResultCreateIndex(self, net):
		self.readErrorInformation(net)

	def createIndex(self, indexDef):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.CREATEINDEX) # createindex command
		self.writeOptions(net)
		net.writeBSON(indexDef)
		net.flush()
		return readResultCreateIndex(net)

	def readResultBackup(self, net):
		result =  self.readInt()
		self.readErrorInformation(net)
		return result

	def backup(self, db, destFile):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.BACKUP) # createindex command
		self.writeOptions(net)
		self.writeString(db)
		self.writeString(destFile)
		net.flush()
		return self.readResultBackup(net)


	def executeQuery(self, net, query):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.EXECUTEQUERY) # executequery command
		self.writeOptions(net)
		net.writeString(query)
		net.flush()

		flag = net.readInt()
		cursorResult = None
		if flag is 1:
			commandType = net.readInt();
			if commandType is CommandType.INSERT:
				self.readResultInsert(net)

			if commandType is CommandType.UPDATE:
				self.readResultUpdate(net)

			if commandType is CommandType.FIND:
				cursorResult = self.readResultFind(net)

			if commandType is CommandType.DROPNAMESPACE:
				self.readResultDropNamespace(net)

			if commandType is CommandType.SHOWDBS:
				dbs = self.readResultShowDbs(net)
				arrDbs = []
				for db in dbs:
					row = {}
					row["db"] = db
					arrDbs.append(row)
				cursorId = None
				cursorResult = cursor.DjondbCursor(net, cursorId, arrDbs)


			if commandType is CommandType.SHOWNAMESPACES:
				nss = self.readResultShowNamespaces(net)
				arrNs = []
				for ns in nss:
					row = {}
					row["ns"] = ns
					arrNs.append(row)
				cursorId = None
				cursorResult = cursor.DjondbCursor(net, cursorId, arrNs)

			if commandType is CommandType.REMOVE:
				self.readResultRemove(net)

			if commandType is CommandType.COMMIT:
				self.readResultCommitTransaction(net)
				self._activeTransactionId = None

			if commandType is CommandType.ROLLBACK:
				self.readResultRollbackTransaction(net)
				self._activeTransactionId = None

			if commandType is CommandType.FETCHCURSOR:
				self.readResultFetchRecords(net)

			if commandType is CommandType.CREATEINDEX:
				return self.readResultCreateIndex(net)

			if commandType is CommandType.BACKUP:
				return self.readResultBackup(net)
		else:
			self.readErrorInformation(net)

		if cursorResult is None:
			arr = []
			row = {}
			row["date"] = str(datetime.date.today())
			row["success"] = True
			arr.append(row)
			cursorResult = cursor.DjondbCursor(net, None, arr)

		return cursorResult


	def executeUpdate(self, net, query):
		net.reset()
		self.writeHeader(net)
		net.writeInt(CommandType.EXECUTEUPDATE) # executeupdate command
		self.writeOptions(net)
		net.writeString(query)
		net.flush()

		flag = net.readInt()
		if flag is 1:
			commandType = net.readInt();
			if commandType is CommandType.INSERT:
				return self.readResultInsert(net)

			if commandType is CommandType.UPDATE:
				return self.readResultUpdate(net)

			if commandType is CommandType.DROPNAMESPACE:
				return self.readResultDropNamespace(net)

			if commandType is CommandType.REMOVE:
				return self.readResultRemove(net)

			if commandType is CommandType.COMMIT:
				res = self.readResultCommitTransaction(net)
				self._activeTransactionId = None
				return res

			if commandType is CommandType.ROLLBACK:
				res = self.readResultRollbackTransaction(net)
				self._activeTransactionId = None
				return res

			if commandType is CommandType.CREATEINDEX:
				return self.readResultCreateIndex(net)

			if commandType is CommandType.BACKUP:
				return self.readResultBackup(net)
		else:
			self.readErrorInformation(net)
		return None


