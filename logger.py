import sqlite3


class logger:
    dbfile = ""

    def __init__(self, dbfile):
        self.dbfile = dbfile

    # @staticmethod
    def add(self, logtext):
        db = sqlite3.connect(self.dbfile)
        cur = db.execute('insert or ignore into logs VALUES(null, "test", null);')
        return cur
