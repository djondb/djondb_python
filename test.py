import pydjondb
con = pydjondb.DjondbConnectionManager.getConnection("localhost");

con.open();

con.insert("testpython", "testns", "{ 'name': 'John' }");

res = con.find("testpython", "testns", "");

print res.toChar();

