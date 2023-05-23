import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

        
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    conn = create_connection(r"./db/database")

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

    if conn is not None:
        create_table(conn, sql_create_user_table)
        create_table(conn, sql_create_message_table)

    else:
        print("Error! cannot create the database connection.")

if __name__ == '__main__':
    main()