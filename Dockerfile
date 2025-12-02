FROM python:3.9-slim

# Устанавливаем curl для healthcheck
RUN apt-get update && apt-get install -y curl postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 8181

ENV FLASK_APP=app.py
ENV FLASK_ENV=production

CMD ["python", "app.py"]
