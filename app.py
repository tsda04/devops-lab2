#!/usr/bin/env python3
from flask import Flask, jsonify
import datetime
import os
import sqlite3
import json

app = Flask(__name__)

def init_database():
    """Инициализация базы данных"""
    db_path = os.getenv('DATABASE_URL', '/data/database.db')
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Создаем таблицу, если её нет
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS visits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        ip_address TEXT
    )
    ''')
    
    # Создаем таблицу для сообщений
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    
    # Добавляем тестовое сообщение, если таблица пустая
    cursor.execute('SELECT COUNT(*) FROM messages')
    if cursor.fetchone()[0] == 0:
        test_messages = [
            ('Welcome to DevOps Lab 4!', datetime.datetime.now().isoformat()),
            ('This is a multi-container application', datetime.datetime.now().isoformat()),
            ('Using Docker Compose with SQLite', datetime.datetime.now().isoformat())
        ]
        cursor.executemany('INSERT INTO messages (message, created_at) VALUES (?, ?)', test_messages)
    
    conn.commit()
    conn.close()

def log_visit(ip_address='unknown'):
    """Логирование посещения"""
    db_path = os.getenv('DATABASE_URL', '/data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO visits (timestamp, ip_address) VALUES (?, ?)',
        (datetime.datetime.now().isoformat(), ip_address)
    )
    
    conn.commit()
    
    # Получаем общее количество посещений
    cursor.execute('SELECT COUNT(*) FROM visits')
    total_visits = cursor.fetchone()[0]
    
    conn.close()
    return total_visits

def get_messages():
    """Получение сообщений из базы данных"""
    db_path = os.getenv('DATABASE_URL', '/data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT message, created_at FROM messages ORDER BY created_at DESC LIMIT 10')
    messages = cursor.fetchall()
    
    conn.close()
    return messages

@app.route('/')
def health():
    # Инициализируем БД при первом запросе
    init_database()
    
    # Логируем посещение
    ip_address = request.remote_addr if hasattr(request, 'remote_addr') else 'unknown'
    total_visits = log_visit(ip_address)
    
    # Получаем сообщения из БД
    messages = get_messages()
    
    return {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'service': 'DevOps Lab 4 - Multi-container App',
        'database': 'SQLite',
        'container_type': 'Docker Compose',
        'total_visits': total_visits,
        'current_ip': ip_address,
        'messages': [
            {'text': msg[0], 'created_at': msg[1]} 
            for msg in messages
        ],
        'endpoints': {
            'health': '/',
            'visits': '/visits',
            'add_message': '/add/<message>'
        }
    }

@app.route('/visits')
def visits():
    """Статистика посещений"""
    db_path = os.getenv('DATABASE_URL', '/data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM visits')
    total_visits = cursor.fetchone()[0]
    
    cursor.execute('SELECT timestamp, ip_address FROM visits ORDER BY timestamp DESC LIMIT 10')
    recent_visits = cursor.fetchall()
    
    conn.close()
    
    return {
        'total_visits': total_visits,
        'recent_visits': [
            {'timestamp': visit[0], 'ip_address': visit[1]}
            for visit in recent_visits
        ]
    }

@app.route('/add/<message>')
def add_message(message):
    """Добавление нового сообщения"""
    db_path = os.getenv('DATABASE_URL', '/data/database.db')
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute(
        'INSERT INTO messages (message, created_at) VALUES (?, ?)',
        (message, datetime.datetime.now().isoformat())
    )
    
    conn.commit()
    conn.close()
    
    return {
        'status': 'message_added',
        'message': message,
        'timestamp': datetime.datetime.now().isoformat()
    }

if __name__ == '__main__':
    # Инициализируем БД при запуске приложения
    init_database()
    app.run(host='0.0.0.0', port=8181, debug=False)
