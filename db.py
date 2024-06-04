import sqlite3 as sql

connection = sql.connect('./User_db.db') # Открытие бд
cursor = connection.cursor()

cursor.execute('''DROP TABLE IF EXISTS User''')
cursor.execute('''
            CREATE TABLE IF NOT EXISTS User (
                id INTEGER PRIMARY KEY,
                name TEXT,
                telegram_name TEXT,
                request TEXT,
                CURRENT_TIME TEXT,
                IS_HOMEWORK_DONE BOOLEAN,
                user_step INTEGER,
                telegram_id TEXT
            )
        ''')

connection.commit()
