"""
  @file    db.py
  @brief   database tools
  @details Copyright (c) 
  @author  Nikolay Vovk
"""

# ===== commands =====
"""
SELECT * FROM cstate WHERE
INSERT INTO cstate VALUES (...) [WHERE ...]
UPDATE cstate SET login = 'g04' WHERE id = 4
DELETE FROM cstate WHERE ...
ALTER TABLE cstate ADD COLUMN containerId TEXT
"""
#=== types ===
"""
id INTEGER PRIMARY KEY, lastTaskId TEXT, autoStop BOOL, createTime DATETIME
"""

import datetime
import sqlite3

import web.logs as logs
DBG = logs.DBG
ERR = logs.ERR

import web.config as config
cfg = config.read()
db_path = cfg.get('db_path', 'db/tmp.db')
db_timeout = cfg.get('db_timeout', 10)

'''
'SELECT proj, count(*) FROM shipment GROUP BY proj' - count of each place
'''

class SQLite3Wrapper:

    def __init__(self, dbPath=db_path):
        DBG.debug('SQLite3Wrapper constructor')
        self.conn = sqlite3.connect(dbPath, timeout=db_timeout)
        self.c = self.conn.cursor()

    def commit(self):
        self.conn.commit()

    def execute(self, sql, *args, **kvargs):
        return self.c.execute(sql, *args, **kvargs)

    # separate updates are slow, better make a lot of in one transaction
    def update(self, sql, *args, **kvargs):
        self.c.execute(sql, *args, **kvargs)
        self.conn.commit()

    def fetchall(self, sql, *args, **kvargs):
        self.execute(sql, *args, **kvargs)
        return self.c.fetchall()

    def createTables(self):
        DBG.info("=== create tables ===")
        try:
            cte = 'CREATE TABLE IF NOT EXISTS '
            ate = 'ALTER TABLE '
            cie = 'CREATE INDEX IF NOT EXISTS index_'
            inc = 'id INTEGER PRIMARY KEY, '

            self.execute(cte + 'credantails' + ' (' + inc + 'user, password, kind)')


            #self.c.execute("CREATE INDEX IF NOT EXISTS index_xml ON xml (id);")
            self.commit()
            print('tables created')
        except Exception as e:
            print(e)
            #ERR.exception('', e)

    def load_credentails(self, creds):
        f = self.fetchall('SELECT user, password FROM credantails')
        for pair in f:
            creds[pair[0]] = pair[1]

 