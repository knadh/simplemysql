#!/usr/bin/env python
# vim: fileencoding=utf-8: noexpandtab

"""
	A very simple wrapper for MySQLdb

	Methods:
		getOne() - get a single row
		getAll() - get all rows
		lastId() - get the last insert id
		lastQuery() - get the last executed query
		insert() - insert a row
		insertOrUpdate() - insert a row or update it if it exists
		update() - update rows
		delete() - delete rows
		query()  - run a raw sql query
		leftJoin() - do an inner left join query and get results

	License: GNU GPLv2

	Kailash Nadh, http://nadh.in
	May 2013
"""

import MySQLdb
from collections import namedtuple

class SimpleMysql:
	conn = None
	cur = None
	conf = None

	def __init__(self, **kwargs):
		self.conf = kwargs
		self.conf["keep_alive"] = kwargs.get("keep_alive", False)
		self.conf["charset"] = kwargs.get("charset", "utf8")
		self.conf["host"] = kwargs.get("host", "localhost")
		self.conf["port"] = kwargs.get("port", 3306)
		self.conf["autocommit"] = kwargs.get("autocommit", False)

		self.connect()

	def connect(self):
		"""Connect to the mysql server"""

		try:
			self.conn = MySQLdb.connect(db=self.conf['db'], host=self.conf['host'],
										port=self.conf['port'], user=self.conf['user'],
										passwd=self.conf['passwd'],
										charset=self.conf['charset'])
			self.cur = self.conn.cursor()
			self.conn.autocommit(self.conf["autocommit"])
		except:
			print ("MySQL connection failed")
			raise


	def getOne(self, table=None, fields='*', where=None, order=None, limit=(0, 1)):
		"""Get a single result

			table = (str) table_name
			fields = (field1, field2 ...) list of fields to select
			where = ("parameterizedstatement", [parameters])
					eg: ("id=%s and name=%s", [1, "test"])
			order = [field, ASC|DESC]
			limit = [limit1, limit2]
		"""

		cur = self._select(table, fields, where, order, limit)
		result = cur.fetchone()

		row = None
		if result:
			Row = namedtuple("Row", [f[0] for f in cur.description])
			row = Row(*result)

		return row


	def getAll(self, table=None, fields='*', where=None, order=None, limit=None):
		"""Get all results

			table = (str) table_name
			fields = (field1, field2 ...) list of fields to select
			where = ("parameterizedstatement", [parameters])
					eg: ("id=%s and name=%s", [1, "test"])
			order = [field, ASC|DESC]
			limit = [limit1, limit2]
		"""

		cur = self._select(table, fields, where, order, limit)
		result = cur.fetchall()

		rows = None
		if result:
			Row = namedtuple("Row", [f[0] for f in cur.description])
			rows = [Row(*r) for r in result]

		return rows

	def lastId(self):
		"""Get the last insert id"""
		return self.cur.lastrowid

	def lastQuery(self):
		"""Get the last executed query"""
		try:
			return self.cur.statement
		except AttributeError:
			return self.cur._last_executed

	def leftJoin(self, tables=(), fields=(), join_fields=(), where=None, order=None, limit=None):
		"""Run an inner left join query

			tables = (table1, table2)
			fields = ([fields from table1], [fields from table 2])  # fields to select
			join_fields = (field1, field2)  # fields to join. field1 belongs to table1 and field2 belongs to table 2
			where = ("parameterizedstatement", [parameters])
					eg: ("id=%s and name=%s", [1, "test"])
			order = [field, ASC|DESC]
			limit = [limit1, limit2]
		"""

		cur = self._select_join(tables, fields, join_fields, where, order, limit)
		result = cur.fetchall()

		rows = None
		if result:
			Row = namedtuple("Row", [f[0] for f in cur.description])
			rows = [Row(*r) for r in result]

		return rows


	def insert(self, table, data):
		"""Insert a record"""

		query = self._serialize_insert(data)

		sql = "INSERT INTO %s (%s) VALUES(%s)" % (table, query[0], query[1])

		return self.query(sql, data.values()).rowcount


	def update(self, table, data, where = None):
		"""Insert a record"""

		query = self._serialize_update(data)

		sql = "UPDATE %s SET %s" % (table, query)

		if where and len(where) > 0:
			sql += " WHERE %s" % where[0]

		return self.query(sql, data.values() + where[1] if where and len(where) > 1 else data.values()
						).rowcount


	def insertOrUpdate(self, table, data, keys):
		insert_data = data.copy()

		data = {k: data[k] for k in data if k not in keys}

		insert = self._serialize_insert(insert_data)

		update = self._serialize_update(data)

		sql = "INSERT INTO %s (%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s" % (table, insert[0], insert[1], update)

		return self.query(sql, insert_data.values() + data.values() ).rowcount

	def delete(self, table, where = None):
		"""Delete rows based on a where condition"""

		sql = "DELETE FROM %s" % table

		if where and len(where) > 0:
			sql += " WHERE %s" % where[0]

		return self.query(sql, where[1] if where and len(where) > 1 else None).rowcount


	def query(self, sql, params = None):
		"""Run a raw query"""

		# check if connection is alive. if not, reconnect
		try:
			self.cur.execute(sql, params)
		except MySQLdb.OperationalError, e:
			# mysql timed out. reconnect and retry once
			if e[0] == 2006:
				self.connect()
				self.cur.execute(sql, params)
			else:
				raise
		except:
			print("Query failed")
			raise

		return self.cur

	def commit(self):
		"""Commit a transaction (transactional engines like InnoDB require this)"""
		return self.conn.commit()

	def is_open(self):
		"""Check if the connection is open"""
		return self.conn.open

	def end(self):
		"""Kill the connection"""
		self.cur.close()
		self.conn.close()

	# ===

	def _serialize_insert(self, data):
		"""Format insert dict values into strings"""
		keys = ",".join( data.keys() )
		vals = ",".join(["%s" for k in data])

		return [keys, vals]


	def _serialize_update(self, data):
		"""Format update dict values into string"""
		return "=%s,".join( data.keys() ) + "=%s"


	def _select(self, table=None, fields=(), where=None, order=None, limit=None):
		"""Run a select query"""

		sql = "SELECT %s FROM `%s`" % (",".join(fields), table)

		# where conditions
		if where and len(where) > 0:
			sql += " WHERE %s" % where[0]

		# order
		if order:
			sql += " ORDER BY %s" % order[0]

			if len(order) > 1:
				sql+= " %s" % order[1]

		# limit
		if limit:
			sql += " LIMIT %s" % limit[0]

			if len(limit) > 1:
				sql+= ", %s" % limit[1]

		return self.query(sql, where[1] if where and len(where) > 1 else None)

	def _select_join(self, tables=(), fields=(), join_fields=(), where=None, order=None, limit=None):
		"""Run an inner left join query"""

		fields = [tables[0] + "." + f for f in fields[0]] + \
				 [tables[1] + "." + f for f in fields[1]]

		sql = "SELECT %s FROM %s LEFT JOIN %s ON (%s = %s)" % \
				( 	",".join(fields),
					tables[0],
					tables[1],
					tables[0] + "." + join_fields[0], \
					tables[1] + "." + join_fields[1]
				)

		# where conditions
		if where and len(where) > 0:
			sql += " WHERE %s" % where[0]

		# order
		if order:
			sql += " ORDER BY %s" % order[0]

			if len(order) > 1:
				sql+= " " + order[1]

		# limit
		if limit:
			sql += " LIMIT %s" % limit[0]

			if len(limit) > 1:
				sql+= ", %s" % limit[1]

		return self.query(sql, where[1] if where and len(where) > 1 else None)

	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.end()