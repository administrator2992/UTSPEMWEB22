import sqlite3

DATABASE_NAME = "db_tekkom_0357.db"

def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn

def create_table_news():
    tables = [
            """CREATE TABLE IF NOT EXISTS
                tbl_news_0357(
                    news_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    datetime TEXT NOT NULL,
                    flag INTEGER NOT NULL)"""
        ]
    
    db = get_db()
    cursor = db.cursor()
    
    for table in tables:
        cursor.execute(table)

def create_table_users():
    tables = [
            """CREATE TABLE IF NOT EXISTS
                tbl_users(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL)"""
        ]
    
    db = get_db()
    cursor = db.cursor()
    
    for table in tables:
        cursor.execute(table)