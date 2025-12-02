#!/usr/bin/env python3
from flask import Flask, jsonify
import datetime
import os
import sqlite3
from pathlib import Path

app = Flask(__name__)

# Конфигурация базы данных
DB_PATH = "/data/app.db"

def init_db():
    """Инициализация базы данных"""
    Path("/data").mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            ip TEXT
        )
    ''')
    conn.commit()
    conn.close()

def log_visit():
    """Логирование посещения"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO visits (timestamp, ip) VALUES (?, ?)",
        (datetime.datetime.now().isoformat(), "0.0.0.0")
    )
    conn.commit()
    conn.close()

def get_visit_count():
    """Получение количества посещений"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM visits")
    count = cursor.fetchone()[0]
    conn.close()
    return count

@app.route('/')
def health():
    # Логируем посещение
    log_visit()
    
    # Получаем статистику
    visit_count = get_visit_count()
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'visits': visit_count,
        'message': 'Docker Compose работает!',
        'db_connected': True
    })

@app.route('/visits')
def visits():
    """Получить все посещения"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM visits ORDER BY timestamp DESC LIMIT 10")
    visits_data = cursor.fetchall()
    conn.close()
    
    return jsonify({
        'total_visits': get_visit_count(),
        'recent_visits': [
            {'id': v[0], 'timestamp': v[1], 'ip': v[2]} 
            for v in visits_data
        ]
    })

if __name__ == '__main__':
    # Инициализируем БД при запуске
    init_db()
    app.run(host='0.0.0.0', port=8181, debug=False)
