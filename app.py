#!/usr/bin/env python3
from flask import Flask
import psycopg2
import os
from datetime import datetime

app = Flask(__name__)

# Получение параметров подключения из переменных окружения
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'lab4db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def init_db():
    """Инициализация базы данных"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Создание таблицы если она не существует
        cur.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP NOT NULL,
                ip VARCHAR(50)
            )
        ''')
        
        conn.commit()
        cur.close()
        conn.close()
        print("База данных инициализирована")
    except Exception as e:
        print(f"Ошибка инициализации БД: {e}")

@app.route('/')
def index():
    """Главная страница - показывает посещения"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Добавляем новое посещение
        cur.execute(
            'INSERT INTO visits (timestamp, ip) VALUES (%s, %s)',
            (datetime.now(), '127.0.0.1')
        )
        
        # Получаем все посещения
        cur.execute('SELECT * FROM visits ORDER BY timestamp DESC')
        visits = cur.fetchall()
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Формируем HTML ответ
        html = '<h1>DevOps Lab 4 - Docker Compose</h1>'
        html += '<h2>Посещения:</h2>'
        html += '<ul>'
        for visit in visits:
            html += f'<li>{visit[1]} - ID: {visit[0]}</li>'
        html += '</ul>'
        html += f'<p>Всего посещений: {len(visits)}</p>'
        
        return html
    except Exception as e:
        return f'<h1>Ошибка подключения к БД</h1><p>{e}</p>'

@app.route('/health')
def health():
    """Health check endpoint"""
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}

if __name__ == '__main__':
    # Инициализируем БД при запуске
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
