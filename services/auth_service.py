import hashlib
from database.db import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(name, phone, email, userid, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO users
    VALUES(?,?,?,?,?,?)
    """,
    (
        name,
        phone,
        email,
        userid,
        hash_password(password),
        1000
    ))

    conn.commit()
    conn.close()

def login_user(userid, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM users
    WHERE userid=? AND password=?
    """,
    (
        userid,
        hash_password(password)
    ))

    user = cur.fetchone()

    conn.close()

    return user

def login_admin(empid,password):

    conn=get_connection()
    cur=conn.cursor()

    cur.execute("""
    SELECT * FROM admins
    WHERE empid=? AND password=?
    """,
    (
        empid,
        hash_password(password)
    ))

    admin=cur.fetchone()

    conn.close()

    return admin