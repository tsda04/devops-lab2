import sqlite3

db = "/data/data.db"

conn = sqlite3.connect(db)
cur = conn.cursor()

# Пересоздаём таблицу при каждом деплое
cur.execute("DROP TABLE IF EXISTS test")
cur.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, message TEXT)")
cur.execute("INSERT INTO test(message) VALUES ('Hello from SQLite DB UPDATED!')")

conn.commit()
conn.close()

print("DB initialized.")
