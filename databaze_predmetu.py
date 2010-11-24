# -*- coding: UTF-8 -*-
import sqlite3

class DB:
	def __init__(self, _dbfile):
		self.conn = sqlite3.connect(_dbfile)
		try:
			self.conn.execute('select * from predmety').close()			
		except sqlite3.Error:
			self.createTable()
	def commit(self):
		# Save (commit) the changes
		self.conn.commit()
	def createTable(self):
		self.conn.execute('create table predmety (predmetid, fakultaid)')
		self.commit()
	def insertInto(self, pid, fid):
		try:
			self.conn.execute('insert into predmety values (?,?)',(pid,fid)).close()
			self.commit()
		except sqlite3.Error, e:
			return False
		return True
	def findFid(self, pid):
		try:
			c = self.conn.execute('select fakultaid from predmety where predmetid=?', (pid,))
			item = c.fetchone()
			c.close()
			try:
				if len(item) == 0 : return None
			except Exception:
				return None
			return item[0]

		except sqlite3.Error, e:
			return None
