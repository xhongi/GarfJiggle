import sqlite3
from sqlite3 import Error

class Database:
    def __init__(self):
        self.databasePath = 'database'
        self.create_db()
    
    def create_db(self):
        sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL
                                    ); """
    
        sql_create_message_table = """CREATE TABLE IF NOT EXISTS message (
                                    id integer PRIMARY KEY,
                                    jiggle integer NOT NULL,
                                    date text NOT NULL,
                                    user_id INTEGER,
                                    FOREIGN KEY (user_id) REFERENCES user (id)
                                );"""
        
        self.execute(sql_create_user_table)
        self.execute(sql_create_message_table)

    def execute(self, query, values=None, fetch=False):
        con = None
        try:
            con = sqlite3.connect(self.databasePath)
            cur = con.cursor()
            if values is None:
                cur.execute(query)
            else:
                cur.execute(query, values)
            con.commit()
            if fetch:
                return cur.fetchall()
        except Error as e:
            print(e)
        