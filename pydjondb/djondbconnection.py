import network
from command import *

class DjondbConnection:
	def __init__(self, host, port = 1423):
		self.host = host
		self.port = port

	def checkError(self, cmd):
		if cmd.resultCode > 0:
			raise DjondbException(cmd.resultCode, cmd.resultMessage)

	def open(self):
		self.network = network.Network()
		self.network.connect("localhost", 1243)

	def showDbs(self):
		cmd = Command()
		res = cmd.showDbs(self.network)
		self.checkError(cmd)
		return res

	def showNamespaces(self, db):
		cmd = Command()
		res = cmd.showNamespaces(self.network, db)
		self.checkError(cmd)
		return res

	def insert(self, db, ns, data):
		cmd = Command()
		res = cmd.insert(self.network, db, ns, data)
		self.checkError(cmd)
		return res

	def update(self, db, ns, data):
		cmd = Command()
		res = cmd.update(self.network, db, ns, data)
		self.checkError(cmd)
		return res

	def find(self, db, ns, select, filter):
		cmd = Command()
		res = cmd.find(self.network, db, ns, select, filter)
		self.checkError(cmd)
		return res

	def dropNamespace(self, db, ns):
		cmd = Command()
		res = cmd.dropNamespace(self.network, db, ns)
		self.checkError(cmd)
		return res

	def remove(self, db, ns, id, revision = None):
		cmd = Command()
		res = cmd.remove(self.network, db, ns, id, revision)
		self.checkError(cmd)
		return res

	def beginTransaction(self):
		self._activeTransactionId = Command().beginTransaction()
		
	def commitTransaction(self):
		cmd = Command()
		cmd.commitTransaction()
		self._activeTransactionId = None
		self.checkError(cmd)
		
	def rollbackTransaction(self):
		cmd = Command()
		cmd.rollbackTransaction()
		self._activeTransactionId = None
		self.checkError(cmd)

	def createIndex(self, indexDef):
		cmd = Command()
		cmd.createIndex(indexDef)
		self.checkError(cmd)

	def executeQuery(self, query):
		cmd = Command()
		res = cmd.executeQuery(self.network, query)
		self.checkError(cmd)
		return res

	def executeUpdate(self, query):
		cmd = Command()
		res = cmd.executeUpdate(self.network, query)
		self.checkError(cmd)
		return res

