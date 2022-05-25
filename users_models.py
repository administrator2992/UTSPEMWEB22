from db import get_db
from flask_bcrypt import Bcrypt
from flask import Flask

app = Flask(__name__)
bcrypt = Bcrypt(app)

# ambil semua data users
def get_users():
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_users"
    cursor.execute(query)
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    
    for row in cursor.fetchall():
        result.append(dict(zip(columns, row))) #konversi ke dictionary
        
    return result

# ambil data students berdasarkan id
def get_users_by_id(id):
    db = get_db()
    cursor = db.cursor()
    #SELECT
    query = "SELECT * FROM tbl_users WHERE id = ?"
    cursor.execute(query, [id])
    columns = [column[0] for column in cursor.description] #ambil nama kolom
    result = []
    result.append(dict(zip(columns, cursor.fetchone()))) #konversi ke dictionary
        
    return result

# menambahkan data users
def insert_users(username, password):
    db = get_db()
    cursor = db.cursor()
    if valuser(username) == True:
        password = bcrypt.generate_password_hash(password)
        query = "INSERT INTO tbl_users(username, password) VALUES (?,?)"
        password = password.decode('utf-8')
        cursor.execute(query, [username, password])
        db.commit()
        return True
    else:
        raise ValueError

# mengubah data users
def update_users(id, username, password):
    db = get_db()
    cursor = db.cursor()    
    password = bcrypt.generate_password_hash(password)
    query = "UPDATE tbl_users SET username = ?, password = ? WHERE id = ?"
    password = password.decode('utf-8')
    cursor.execute(query, [username, password, id])
    db.commit()
    return True

# menghapus data users
def delete_users(id):
    db = get_db()
    cursor = db.cursor()
    query = "DELETE FROM tbl_users WHERE id = ?"
    cursor.execute(query, [id])
    db.commit()
    return True

# validate username taken or not yet
def valuser(username):
    db = get_db()
    cursor = db.cursor()
    query = "SELECT * FROM tbl_users WHERE username = ?"
    cursor.execute(query, [username])
    if cursor.fetchone() == None:
        return True
    else:
        return False