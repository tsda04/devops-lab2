# Используем официальный Python образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY app.py .

# Открываем порт, который использует приложение
EXPOSE 8181

# Переменные окружения
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Команда для запуска приложения
CMD ["python", "app.py"]
