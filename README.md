#SimpleMysql
An ultra simple wrapper for Python MySQLdb with very basic functionality

- Kailash Nadh, June 2013
- Documentation: [http://nadh.in/code/simplemysql](http://nadh.in/code/simplemysql)
- License: GPL v2

## Installation
With pip or easy_install

```pip install simplemysql``` or ```easy_install simplemysql```

Or from the source

```python setup.py install```

#Usage
#For normal connection
```python
from simplemysql import SimpleMysql

db = SimpleMysql(
	host="127.0.0.1",
	db="mydatabase",
	user="username",
	passwd="password",
	keep_alive=True # try and reconnect timedout mysql connections?
)
```
#For SSL Connection 
```python
from simplemysqlssl import SimpleMysql

db = SimpleMysql(
    host="127.0.0.1",
    db="mydatabase",
    user="username",
    passwd="password",
    ssl = {'cert': 'client-cert.pem', 'key': 'client-key.pem'},
    keep_alive=True # try and reconnect timedout mysql connections?
)

```


```python
# insert a record to the <em>books</em> table
db.insert("books", {"type": "paperback", "name": "Time Machine", "price": 5.55, year: "1997"})

book = db.getOne("books", ["name"], ["year = 1997"])

print "The book's name is " + book.name
```

#Query methods
insert(), update(), delete(), getOne(), getAll(), lastId(), query()

##insert(table, record{})
Inserts a single record into a table.

```python
db.insert("food", {"type": "fruit", "name": "Apple", "color": "red"})
db.insert("books", {"type": "paperback", "name": "Time Machine", "price": 5.55})
```

##update(table, row{}, condition[])
Update one more or rows based on a condition (or no condition).

```python
# update all rows
db.update("books", {"discount": 0})

# update rows based on a simple hardcoded condition
db.update("books",
	{"discount": 10},
	["id=1"]
)

# update rows based on a parametrized condition
db.update("books",
	{"discount": 10},
	("id=%s AND year=%s", [id, year])
)
```

##insertOrUpdate(table, row{}, key)
Insert a new row, or update if there is a primary key conflict.

```python
# insert a book with id 123. if it already exists, update values
db.insert("books",
		{"id": 123, type": "paperback", "name": "Time Machine", "price": 5.55},
		"id"
)
```

##getOne(table, fields[], condition[], order[], limit[])
##getAll(table, fields[], condition[], order[], limit[])
Get a single record or multiple records from a table given a condition (or no condition). The resultant rows are returned as namedtuples. getOne() returns a single namedtuple, and getAll() returns a list of namedtuples.

```python
book = db.getOne("books", ["id", "name"])
```

```python
# get a row based on a simple hardcoded condition
book = db.getOne("books", ["name", "year"], ("id=1"))
```

```python
# get a row based on a simple hardcoded condition
book = db.getOne("books", ["name", "year"], ("id=1"))
```

```python
# get multiple rows based on a parametrized condition
books = db.getAll("books",
	["id", "name"],
	("year > %s and price < 15", [year, 12.99])
)
```

```python
# get multiple rows based on a parametrized condition with an order and limit specified
books = db.getAll("books",
	["id", "name", "year"],
	("year > %s and price < 15", [year, 12.99]),
	["year", "DESC"],	# ORDER BY year DESC
	[0, 10]			# LIMIT 0, 10
)
```
# lastId()
Get the last insert id

# lastQuery()
Get the last query executed

# delete(table, fields[], condition[], order[], limit[])
Delete one or more records based on a condition (or no condition)

```python
# delete all rows
db.delete("books")

# delete rows based on a condition
db.delete("books", ("price > %s AND year < %s", [25, 1999]))
```

##query(table)
Run a raw SQL query. The MySQLdb cursor is returned.

```python
db.query("DELETE FROM books WHERE year > 2005")
```

# commit()
Insert, update, and delete operations on transactional databases such as innoDB need to be committed
