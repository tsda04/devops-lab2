FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY db.py .

# Персистентные данные
VOLUME /data

EXPOSE 8181

CMD ["sh", "-c", "python db.py && python app.py"]
