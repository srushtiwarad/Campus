import sqlite3

conn = sqlite3.connect("complaint.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    role TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS complaints (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student TEXT,
    title TEXT,
    category TEXT,
    description TEXT,
    status TEXT
)
""")

conn.commit()
conn.close()
print("Database created successfully")
