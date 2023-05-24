from database import Database

db = Database()

def select_garf_ranking():
    query = '''
        SELECT user.name, COUNT(*) AS count
        FROM message INNER JOIN user
        ON user.id = message.user_id
        WHERE message.jiggle = 0
        GROUP BY message.user_id
        ORDER BY 2 DESC
        LIMIT 10;'''
    
    result = db.execute(query, fetch=True)

    for i, row in enumerate(result):
        print(f'{i+1}. {row[0]} - {row[1]}')

def select_jiggle_ranking():
    query = '''
        SELECT user.name, COUNT(*) AS count
        FROM message INNER JOIN user
        ON user.id = message.user_id
        WHERE message.jiggle = 1
        GROUP BY message.user_id
        ORDER BY 2 DESC
        LIMIT 10;'''
    
    result = db.execute(query, fetch=True)

    for i, row in enumerate(result):
        print(f'{i+1}. {row[0]} - {row[1]}')

print("TOP 10 JIGGLERS")
select_jiggle_ranking()

print(f'\nTOP 10 GARFERS')
select_garf_ranking()