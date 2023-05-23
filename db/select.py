import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_messages(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM message INNER JOIN user ON user.id = message.user_id")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def select_all_users(conn):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_jiggler_ranking(conn):
    cur = conn.cursor()

    sql = '''
        SELECT user.name, COUNT(*) AS count
        FROM message INNER JOIN user
        ON user.id = message.user_id
        WHERE message.jiggle = 1
        GROUP BY message.user_id
        ORDER BY 2 DESC;
    '''

    cur.execute(sql)

    rows = cur.fetchall()
    for row in rows[:10]:
        print(row)

def select_garf_ranking(conn):
    cur = conn.cursor()

    sql = '''
        SELECT user.name, COUNT(*) AS count
        FROM message INNER JOIN user
        ON user.id = message.user_id
        WHERE message.jiggle = 0
        GROUP BY message.user_id
        ORDER BY 2 DESC;
    '''

    cur.execute(sql)

    rows = cur.fetchall()
    for row in rows[:10]:
        print(row)


def main():
    database = './db/database'

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("TOP 10 JIGGLERS")
        select_jiggler_ranking(conn)

        print(f'\nTOP 10 GARFERS')
        select_garf_ranking(conn)


if __name__ == '__main__':
    main()