import network
from command import *

class DjondbConnection:
	def __init__(self, host, port = 1423):
		self.host = host
		self.port = port

	def open(self):
		self.network = network.Network()
		self.network.connect("localhost", 1243)

	def showDbs(self):
		return Command().showDbs(self.network)

	def showNamespaces(self, db):
		return Command().showNamespaces(self.network, db)

	def insert(self, db, ns, data):
		return Command().insert(self.network, db, ns, data)

	def update(self, db, ns, data):
		return Command().update(self.network, db, ns, data)

	def find(self, db, ns, select, filter):
		return Command().find(self.network, db, ns, select, filter)

	def dropNamespace(self, db, ns):
		return Command().dropNamespace(self.network, db, ns)

	def remove(self, db, ns, id, revision = None):
		return Command().remove(self.network, db, ns, id, revision)

	def beginTransaction(self):
		self._activeTransactionId = Command().beginTransaction()
		
	def commitTransaction(self):
		Command().commitTransaction()
		self._activeTransactionId = None
		
	def rollbackTransaction(self):
		Command().rollbackTransaction()
		self._activeTransactionId = None

	def createIndex(self, indexDef):
		Command().createIndex(indexDef)

