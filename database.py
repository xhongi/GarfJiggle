import sqlite3
from sqlite3 import Error
from time import gmtime, strftime

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
    
    def get_current_time(self):
        return strftime("%Y-%m-%d %H:%M:%S", gmtime())

    def add_user(self, username):
        query = '''
            INSERT INTO user(name) VALUES(?);
            '''
        self.execute(query, values=(username,))

    def select_jiggle_ranking(self):
        query = '''
            SELECT user.name, COUNT(*) AS count
            FROM message INNER JOIN user
            ON user.id = message.user_id
            WHERE message.jiggle = 1
            GROUP BY message.user_id
            ORDER BY 2 DESC
            LIMIT 10;'''

        result = self.execute(query, fetch=True)

        return result

    def select_garf_ranking(self):
        query = '''
            SELECT user.name, COUNT(*) AS count
            FROM message INNER JOIN user
            ON user.id = message.user_id
            WHERE message.jiggle = 0
            GROUP BY message.user_id
            ORDER BY 2 DESC
            LIMIT 10;'''

        result = self.execute(query, fetch=True)
        
        return result

    def get_user_id(self, username):
        query = '''SELECT * FROM user WHERE name = ?;'''
        result = self.execute(query, values=(username, ), fetch=True)

        # In case user doesnt exist
        if len(result) == 0:
            self.add_user(username)
            return self.get_user_id(username)

        return result[0][0]

    def add_jiggler(self, username):
        id = self.get_user_id(username)

        query = '''
            INSERT INTO message(jiggle, date, user_id) VALUES (?, ?, ?)
        '''

        self.execute(query, values=(1, self.get_current_time(), id))

    def add_garfer(self, username):
        id = self.get_user_id(username)

        query = '''
            INSERT INTO message(jiggle, date, user_id) VALUES (?, ?, ?)
        '''

        self.execute(query, values=(0, self.get_current_time(), id))