import sqlite3

db = sqlite3.connect("users.db", check_same_thread=False)
cur = db.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
  username TEXT UNIQUE,
  password TEXT
)
""")
db.commit()
