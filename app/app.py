from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

DB_FILE = "/data/data.db"

@app.route("/")
def index():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT message FROM test LIMIT 1;")
    row = cur.fetchone()
    conn.close()

    return jsonify({"db_message": row[0] if row else "empty"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181)
