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

con.insert("testdb", "testns", r)

cursor = con.find("testdb", "testns", "*", "")
elementToRemove = None
while cursor.next():
	item = cursor.current()
	elementToRemove = item
	print(json.dumps(item))

con.remove("testdb", "testns", item["_id"], item["_revision"])

con.dropNamespace("testdb", "testns")


