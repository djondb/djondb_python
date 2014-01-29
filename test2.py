import pydjondb

con = pydjondb.DjondbConnectionManager.getConnection('localhost');
con.open();

hero = "{ name: 'Peter', lastName: 'Parker', occupations: [ { company: 'Daily Bugle', position: 'Photographer'}, { position: 'Superhero' } ], nicknames: [{ name: 'Spiderman', main: 1}, {'name': 'Spidey'}] }"

con.insert("test_python", "superheroes", hero);

print "inserted"

cursor = con.find("test_python", "superheroes", "$'name' == 'Peter'");

print "find"

while cursor.next() :
	r = cursor.current()
	print r.getString("name"), r.toChar()

pydjondb.DjondbConnectionManager.releaseConnection(con);
