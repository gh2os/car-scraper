import sqlite3

def create_connection():
    connection = sqlite3.connect('scraper_data.db')
    return connection

def setup_database():
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY,
            source TEXT NOT NULL,
            title TEXT NOT NULL,
            price TEXT,
            url TEXT NOT NULL
        )
    ''')
    connection.commit()
    connection.close()
