'''
Created on Dec 29, 2014

@author: ericrudisill
'''
import sqlite3

class BitStormDb(object):

    def __init__(self):
        self.db = sqlite3.connect('./bitstorm.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
        self.initDb()

    def initDb(self):
        c = self.db.cursor()
        
        # Create records table
        c.execute("SELECT * FROM sqlite_master WHERE name ='records' and type='table';")
        result = c.fetchone()
        if result == None:
            self.db.execute('''
                            CREATE TABLE records(ts timestamp, mac varchar, rssi int, temp int, batt int, batt_hex varchar, cs int, router varchar, messageType int, nodeType int)
                            ''')
            self.db.commit()
        c.close()

    def close(self):
        self.db.close()
        
    def insertRecord(self, record):
        c = self.db.cursor()
        c.execute("insert into records values(?,?,?,?,?,?,?)", \
                  (record.ts, record.mac, record.rssi, record.temp, \
                   record.batt, record.batt_hex, record.cs))
        self.db.commit()
        c.close()
        
    def insertAppMessageRecord(self, record):
        mac = "{0:016x}".format(record.extAddr)
        router = "{0:016x}".format(record.routerAddr)
        c = self.db.cursor()
        c.execute("insert into records values(?,?,?,?,?,?,?,?,?,?)", \
                  (record.ts, mac, record.rssi, record.temperature, \
                   record.battery, hex(record.battery), record.cs, router, \
                   record.messageType, record.nodeType))
        self.db.commit()
        c.close()        