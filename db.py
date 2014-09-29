import sqlite3

class Db(object):
	'''
	classdocs
	'''
	conn = None
	cur = None
	conf = None


	def __init__(self, **kwargs):
		self.conf = kwargs
		self.conf["database"] = kwargs.get("database", "rotamaker.db")
		self.conf["detect_types"] = kwargs.get("detect_types", sqlite3.PARSE_DECLTYPES)

		self._connect()
		

	def _queryable(f):
		def new_f(self, *args, **kwargs):
			sql, params = f(self, *args, **kwargs)
			self._query(sql, params)
			return self.cur.fetchall() if f.func_name == "select" else self.cur.rowcount
		return new_f


	@_queryable
	def select(self, table, fields='*', where=None):
		sql = "SELECT {0} FROM {1}".format(", ".join(fields), table)
		if where:
			sql += " WHERE" + " AND ".join([" {0} = ?".format(k) for k in where.keys()])
		sql += ";"

		params = tuple(where.values()) if where else None

		return sql, params


	@_queryable
	def insert(self, table, fields):
		sql = "INSERT INTO {0}".format(table) \
			+ " ({0}) ".format(",".join([k for k in fields.keys()])) \
			+ "VALUES ({0});".format(",".join("?"*len(fields)))

		params = tuple(fields.values())

		return sql, params


	@_queryable
	def update(self, table, fields, where):
		sql = "UPDATE {0} SET".format(table) \
		    + ",".join([" {0} = ?".format(k) for k in fields.keys()]) \
			+ " WHERE " + " AND ".join([" {0} = ?".format(k) for k in where.keys()]) \
			+ ";"

		params = tuple(fields.values()) + tuple(where.values())

		return sql, params


	@_queryable
	def delete(self, table, where):
		sql = "DELETE FROM {0} WHERE".format(table) \
			+ " AND ".join([" {0} = ?".format(k) for k in where.keys()]) \
			+ ";"

		params = tuple(where.values())

		return sql, params


	def _query(self, sql, params=None):
		''' Executes a raw sql query. '''
		try:
			self.cur.execute(sql, params) if params else self.cur.execute(sql)
			self.conn.commit()
		except Exception, e:
			self.conn.rollback()
			print("Error executing query: ", sql)
			raise e


	def _connect(self):
		''' Connect to Sqlite database. '''
		self.conn = sqlite3.connect(self.conf["database"], detect_types=self.conf["detect_types"])
		self.conn.row_factory = sqlite3.Row # This allows to access columns by index or by insensitive case name.
		self.cur = self.conn.cursor()


	def _disconnect(self):
		''' Disconnect from Sqlite database. '''
		self.cur.close()
		self.conn.close()


	def __enter__(self):
		return self


	def __exit__(self):
		self._disconnect()


if __name__ == '__main__':
	conn = sqlite3.connect('rotamaker.db', detect_types=sqlite3.PARSE_DECLTYPES)
	c = conn.cursor()

	c.execute('''CREATE TABLE IF NOT EXISTS workers (
					partner_id  	INTEGER PRIMARY KEY NOT NULL,
					name			TEXT 	NOT NULL,
					category		INTEGER NOT NULL,
					contract_hrs	NUMERIC NOT NULL,
					max_hrs			NUMERIC NOT NULL
				) WITHOUT ROWID;''')

	c.execute('''CREATE TABLE IF NOT EXISTS shifts (
					s_date		DATE 	NOT NULL,
					start_time	TEXT	NOT NULL,
					end_time	TEXT 	NOT NULL,
					category	INTEGER NOT NULL,
					partner_id	INTEGER,
					FOREIGN KEY(partner_id) REFERENCES workers(partner_id)
				);''')

	workers = [(1, 'Josh', 1, 40, 48),
    		   (2, 'Lina', 2, 32, 40),
    		   (3, 'Dagmara', 2, 32, 40),
    		   (4, 'Rasa', 2, 20, 28),
    		   (5, 'Emma', 3, 36, 48),
    		   (6, 'Filipe', 3, 32, 40),
    		   (7, 'Patrycia', 3, 32, 40),
    		   (8, 'Joanna', 3, 10, 18),
    		   (9, 'Jose', 3, 20, 28)]

	c.executemany("INSERT INTO workers VALUES(?,?,?,?,?);", workers)
	conn.commit()

