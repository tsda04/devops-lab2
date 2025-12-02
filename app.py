#!/usr/bin/env python3
from flask import Flask
import psycopg2
import os
from datetime import datetime
import time

app = Flask(__name__)

# Получение параметров подключения из переменных окружения
DB_HOST = os.getenv('DB_HOST', 'db')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'lab4db')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

def wait_for_db():
    """Ждем пока база данных станет доступной"""
    max_attempts = 30
    for i in range(max_attempts):
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            conn.close()
            print("✅ Database connection successful!")
            return True
        except Exception as e:
            print(f"⏳ Waiting for database... (attempt {i+1}/{max_attempts})")
            time.sleep(2)
    return False

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
                timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                ip VARCHAR(50)
            )
        ''')
        
        # Вставляем тестовую запись
        cur.execute(
            'INSERT INTO visits (timestamp, ip) VALUES (%s, %s)',
            (datetime.now(), 'initial')
        )
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ Database initialized successfully!")
    except Exception as e:
        print(f"❌ Database initialization error: {e}")

@app.route('/')
def index():
    """Главная страница - показывает посещения"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Добавляем новое посещение
        cur.execute(
            'INSERT INTO visits (timestamp, ip) VALUES (CURRENT_TIMESTAMP, %s)',
            ('web',)
        )
        
        # Получаем все посещения
        cur.execute('SELECT id, timestamp, ip FROM visits ORDER BY timestamp DESC LIMIT 20')
        visits = cur.fetchall()
        
        # Получаем общее количество
        cur.execute('SELECT COUNT(*) FROM visits')
        total = cur.fetchone()[0]
        
        conn.commit()
        cur.close()
        conn.close()
        
        # Формируем HTML ответ
        html = '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>DevOps Lab 4 - Docker Compose</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; }
                h1 { color: #333; }
                table { border-collapse: collapse; width: 100%; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .status { color: green; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>🚀 DevOps Lab 4 - Docker Compose</h1>
            <p class="status">✅ Application is running with PostgreSQL database</p>
            <p>Total visits: <strong>{}</strong></p>
            <h2>Recent visits:</h2>
            <table>
                <tr><th>ID</th><th>Timestamp</th><th>IP</th></tr>
                {}
            </table>
            <p><small>Auto-refresh every 30 seconds</small></p>
            <script>
                setTimeout(() => location.reload(), 30000);
            </script>
        </body>
        </html>
        '''
        
        rows = ''
        for visit in visits:
            rows += f'<tr><td>{visit[0]}</td><td>{visit[1]}</td><td>{visit[2]}</td></tr>'
        
        return html.format(total, rows)
    except Exception as e:
        return f'''
        <h1>❌ Database Connection Error</h1>
        <p>Error: {e}</p>
        <p>Connection details: {DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}</p>
        '''

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        return {
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, 500

@app.route('/ready')
def ready():
    """Readiness probe"""
    return {'ready': True}, 200

if __name__ == '__main__':
    print("🚀 Starting Flask application...")
    
    # Ждем пока база данных станет доступной
    if wait_for_db():
        init_db()
        print("✅ Starting Flask server on port 5000")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        print("❌ Failed to connect to database after 30 attempts")
        print("💡 Check if PostgreSQL container is running and healthy")
