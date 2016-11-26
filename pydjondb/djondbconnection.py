import network
from command import *

class DjondbConnection:
	def __init__(self, host, port = 1423):
		self.host = host
		self.port = port
		self.cmd = Command()

	def checkError(self, cmd):
		if self.cmd.resultCode > 0:
			raise DjondbException(self.cmd.resultCode, self.cmd.resultMessage)

	def open(self):
		self.network = network.Network()
		self.network.connect(self.host, self.port)

	def showDbs(self):
		res = self.cmd.showDbs(self.network)
		self.checkError(self.cmd)
		return res

	def showNamespaces(self, db):
		res = self.cmd.showNamespaces(self.network, db)
		self.checkError(self.cmd)
		return res

	def insert(self, db, ns, data):
		res = self.cmd.insert(self.network, db, ns, data)
		self.checkError(self.cmd)
		return res

	def update(self, db, ns, data):
		res = self.cmd.update(self.network, db, ns, data)
		self.checkError(self.cmd)
		return res

	def find(self, db, ns, select, filter):
		res = self.cmd.find(self.network, db, ns, select, filter)
		self.checkError(self.cmd)
		return res

	def dropNamespace(self, db, ns):
		res = self.cmd.dropNamespace(self.network, db, ns)
		self.checkError(self.cmd)
		return res

	def remove(self, db, ns, id, revision = None):
		res = self.cmd.remove(self.network, db, ns, id, revision)
		self.checkError(self.cmd)
		return res

	def beginTransaction(self):
		self._activeTransactionId = self.cmd.beginTransaction()
		
	def commitTransaction(self):
		self.cmd.commitTransaction(self.network)
		self._activeTransactionId = None
		self.checkError(self.cmd)
		
	def rollbackTransaction(self):
		self.cmd.rollbackTransaction(self.network)
		self._activeTransactionId = None
		self.checkError(self.cmd)

	def createIndex(self, indexDef):
		self.cmd.createIndex(indexDef)
		self.checkError(self.cmd)

	def executeQuery(self, query):
		res = self.cmd.executeQuery(self.network, query)
		self.checkError(self.cmd)
		return res

	def executeUpdate(self, query):
		res = self.cmd.executeUpdate(self.network, query)
		self.checkError(self.cmd)
		return res

