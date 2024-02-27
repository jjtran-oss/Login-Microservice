import sqlite3
import hashlib

conn = sqlite3.connect("userdata.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS userdata (
            id INTEGER PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL)
            """)

username1, password1 = "fakeuser", hashlib.sha256("12345".encode()).hexdigest()
cur.execute("INSERT INTO userdata (username, password) VALUES (?, ?)", (username1, password1))

conn.commit()

print(username1, password1)