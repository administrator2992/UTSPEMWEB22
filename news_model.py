from db import get_db
import datetime

# ambil semua data news
def get_news():
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_news_0357"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row))) #konversi ke dictionary
    return result

def get_news_user():
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_news_0357 WHERE flag = 1"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row))) #konversi ke dictionary
    return result

# ambil data news berdasarkan id
def get_news_by_id(news_id):
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_news_0357 WHERE news_id = ?"
    cursor.execute(query, [news_id])
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    result.append(dict(zip(columns, cursor.fetchone()))) #konversi ke dictionary
    result = result[0]
    return result

# ambil data news berdasarkan id
def get_news_by_id_user(news_id):
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_news_0357 WHERE news_id = ? AND flag = 1"
    cursor.execute(query, [news_id])
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    result.append(dict(zip(columns, cursor.fetchone()))) #konversi ke dictionary
    result = result[0]
    return result

# menambahkan data news
def insert_news(title, content, flag):
    if valtitle(title) == True:
        if valflag(flag) == True:
            db = get_db()
            cursor = db.cursor()
            query = "INSERT INTO tbl_news_0357(title, content, datetime, flag) VALUES (?,?,?,?)"
            cursor.execute(query, [title, content, str(datetime.datetime.now()), flag])
            db.commit()
            return True
    else: return False

# mengubah data news
def update_news(news_id, title, content, flag):
    if valflag(flag) == True:
        db = get_db()
        cursor = db.cursor()
        query = "UPDATE tbl_news_0357 SET title = ?, content = ?, datetime = ?, flag = ? WHERE news_id = ?"
        cursor.execute(query, [title, content, str(datetime.datetime.now()), flag, news_id])
        db.commit()
        return True
    else: return False

def patch_news(news_id, flag):
    db = get_db()
    cursor = db.cursor()
    if valflag(flag) == True: 
        query = "UPDATE tbl_news_0357 SET flag = ? WHERE news_id = ?"
        cursor.execute(query, [flag, news_id])
        db.commit()
        return True
    else: return False

# menghapus data news
def delete_news(news_id):
    db = get_db()
    cursor = db.cursor()
    query = "DELETE FROM tbl_news_0357 WHERE news_id = ?"
    cursor.execute(query, [news_id])
    db.commit()
    return True

# validate title taken or not yet
def valtitle(title):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM tbl_news_0357 WHERE title = ?"
    cursor.execute(query, [title])
    if cursor.fetchone() == None:
        return True
    else:
        return False

# validate flag
def valflag(flag):
    if flag == 1 or flag == 2 or flag == 0:
        return True
    else:
        return False