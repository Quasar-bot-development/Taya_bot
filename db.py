import sqlite3 as sql

connection = sql.connect('./User_db.db') # Открытие бд
cursor = connection.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS last_message_time (
                id INTEGER PRIMARY KEY,
                time INTEGER,
                chat_id INTEGER
            )
        ''')

connection.commit()