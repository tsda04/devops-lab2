# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Устанавливаем системные зависимости для SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY app.py .

# Создаем директорию для данных
RUN mkdir -p /data

# Открываем порт, который использует приложение
EXPOSE 8181

# Переменные окружения
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV DATABASE_URL=/data/database.db

# Команда для запуска приложения
CMD ["python", "app.py"]
