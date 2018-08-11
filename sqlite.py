import sqlite3


class Sqlite:
    
    def __init__(self, db_file):
        self.db = sqlite3.connect(db_file, check_same_thread=False)
    
    def close_connection(self):
        if self.db is not None:
            self.db.close()
    
    def select_all(self, table):
        cur = self.db.cursor()
        cur.execute('SELECT * FROM ' + table)
        rows = cur.fetchall()
        return rows
    
    def select_by(self, sql):
        try:
            cur = self.db.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows
        except Exception as e:
            return e
    
    def insert(self, table, data):
        cur = self.db.cursor()
        sql = 'INSERT INTO ' + table + ' VALUES ' + data
        try:
            cur.execute(sql)
            self.db.commit()
            return True
        except Exception as e:
            return e