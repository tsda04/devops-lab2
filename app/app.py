from flask import Flask, jsonify, request, render_template_string
import sqlite3

app = Flask(__name__)
DB_FILE = "/data/data.db"

# HTML-шаблон фронта
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Users</title>
</head>
<body>
    <h1>Users</h1>
    <ul id="users-list">
        {% for user in users %}
        <li>{{ user['id'] }} - {{ user['name'] }}</li>
        {% endfor %}
    </ul>

    <h2>Add User</h2>
    <input type="text" id="username" placeholder="Enter name">
    <button onclick="addUser()">Add</button>

    <script>
        function addUser() {
            const name = document.getElementById('username').value;
            fetch('/users', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({name})
            })
            .then(response => response.json())
            .then(data => {
                const ul = document.getElementById('users-list');
                const li = document.createElement('li');
                li.textContent = data.id + " - " + data.name;
                ul.appendChild(li);
                document.getElementById('username').value = '';
            });
        }
    </script>
</body>
</html>
"""

# Получение всех пользователей
@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users")
    rows = cur.fetchall()
    conn.close()
    users = [{"id": r[0], "name": r[1]} for r in rows]
    return jsonify(users)

# Добавление нового пользователя
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Name is required"}), 400

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("INSERT INTO users(name) VALUES (?)", (name,))
    conn.commit()
    user_id = cur.lastrowid
    conn.close()
    return jsonify({"id": user_id, "name": name})

@app.route("/")
def index():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users")
    rows = cur.fetchall()
    conn.close()
    users = [{"id": r[0], "name": r[1]} for r in rows]
    return render_template_string(HTML_TEMPLATE, users=users)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181)
