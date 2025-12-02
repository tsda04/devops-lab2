import sqlite3

db = "/data/data.db"

conn = sqlite3.connect(db)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, message TEXT)")
cur.execute("INSERT INTO test(message) VALUES ('Hello from SQLite DB!')")
conn.commit()
conn.close()

print("DB initialized.")
