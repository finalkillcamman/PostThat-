from passlib.hash import bcrypt
from database import cur, db

def register(username, password):
    cur.execute(
        "INSERT INTO users VALUES (?,?)",
        (username, bcrypt.hash(password))
    )
    db.commit()

def verify(username, password):
    cur.execute("SELECT password FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    return row and bcrypt.verify(password, row[0])
