import pydjondb
con = pydjondb.DjondbConnectionManager.getConnection("localhost");

con.open();

con.insert("testpython", "testns", "{ 'name': 'John' }");

res = con.find("testpython", "testns", "");

res.next();
obj = res.current();

print obj.toChar();


try:
	con.update("testpython", "testns", "{ '_id': '1234', '_revision': '1234' }");
except e:
	print(e)

