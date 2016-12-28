import unittest
from djondbconnection import *
from bson import *
import json

host = "localhost"
port = 1243

# buffer = network.int_toendian(10)
# print(repr(buffer))
# val = network.int_fromendian(buffer, 0)
# print(val)

con = DjondbConnection(host, port)
con.open()

class TestPyDjondb(unittest.TestCase):
	def testInsert(self):
		print('testInsert')
		con.dropNamespace('testdb', 'testns')

		con.insert('testdb', 'testns', { 'name': 'John', 'address': { 'type': 'home', 'number': 10, 'street': 'Ave 123' } })

		c = con.find('testdb', 'testns', '*', '')
		assert c.next(), 'find should return 1 record after the insert'
		name = c.current()['name']
		assert c.current()['name'] == 'John', 'Name should have John'
		print('~testInsert')

#	def testInsertWithArrays(self):
#		print('testInsertWithArrays')
#		con.dropNamespace('testdb', 'testns')
#
#		con.insert('testdb', 'testns', { 'name': 'John', 'address': { 'type': 'home', 'number': 10, 'street': 'Ave 123', "array": [{"test": "Blah"}] } })
#
#		c = con.find('testdb', 'testns', '*', '')
#		assert c.next(), 'find should return 1 record after the insert'
#		array = c.current()['array']
#		self.assertIsNotNone(array)
#		assert c.current()['array'] == 'John', 'Name should have John'
#		print('~testInsertWithArrays')

	def testUpdate(self):
		print('testUpdate')
		con.dropNamespace('testdb', 'testns')

		con.insert('testdb', 'testns', { 'name': 'John', 'address': { 'type': 'home', 'number': 10, 'street': 'Ave 123' } })

		c = con.find('testdb', 'testns', '*', '')
		assert c.next(), 'find should return 1 record after the insert'
		record = c.current()
		record['age'] = 20
		con.update('testdb', 'testns', record)

		c = con.find('testdb', 'testns', '*', '')
		assert c.next(), 'find should return 1 record after the update'
		record = c.current()
		assert record['age'] is 20
		print('~testUpdate')

	def testDQL(self):
		print('testDQL')
		con.executeQuery('drop ns "testdb", "testns"')
		data = { 'name': 'John', 'age': 20, 'address': { 'type': 'home', 'number': 10, 'street': 'Ave 123' } }
		con.executeQuery('insert %s into %s:%s' % (json.dumps(data), 'testdb', 'testns'))

		cur = con.executeQuery('select * from %s:%s' % ('testdb', 'testns'))
		assert cur.next(), 'select should return at least one record'
		record = cur.current()
		assert record['age'] is 20

		print('testing wrong parse')
		try:
			con.executeQuery('select bl bla x where')
			raise Exception('Expecting an error')
		except DjondbException as e:
			pass
		print('~testDQL')


	def testShowDBs(self):
		print('testShowDBs')
		dbs = con.executeQuery('show databases')
		print('~testShowDBs')

	def testOthers(self):
		print("testOthers")
		result = con.showDbs()

		print("ShowDBS")
		print(result)

		result = con.showNamespaces("testdb")
		print("ShowNamespaces")
		print(result)

		r = {}
		r["name"] = "John"
		r["lastName"] = "John"

		for k in r.keys():
			print("key: %s, type: %s" % (k, type(r[k])))

		print("test insert")
		con.insert("testdb", "testns", r)

		print("test find")
		cursor = con.find("testdb", "testns", "*", "")
		elementToRemove = None
		print("iterating cursor")
		while cursor.next():
			item = cursor.current()
			elementToRemove = item
			print(json.dumps(item))

		print("removing elements")
		con.remove("testdb", "testns", item["_id"], item["_revision"])

		# test unexisting element
		print("removing unexisting elements")
		try:
			result = con.remove("testdb", "testns", "ablch", item["_revision"])
		except:
			pass

		print("dropping namespace")
		con.dropNamespace("testdb", "testns")

		print("testing dql")
		con.executeQuery("insert {'name': 'John' } into TestDB:TestDQL")
		cursor = con.executeQuery("select * from TestDB:TestDQL")
		while cursor.next():
			item = cursor.current()
			print(json.dumps(item))
		print("~testOthers")

	def testTransaction(self):
		print("testTransaction")
		con.beginTransaction()

		con.insert('TestDB', 'TestTX', { "name": "Test" })
		con.commitTransaction()

		con.beginTransaction()
		con.insert('TestDB', 'TestTX', { "name": "Test2" })
		con.rollbackTransaction()
		print("~testTransaction")


if __name__ == '__main__':
	unittest.main()
