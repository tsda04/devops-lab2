-- Создаем базу данных
CREATE DATABASE appdb;

-- Создаем пользователя
CREATE USER appuser WITH ENCRYPTED PASSWORD 'apppassword';

-- Даем права пользователю
GRANT ALL PRIVILEGES ON DATABASE appdb TO appuser;

-- Подключаемся к базе данных
\c appdb

-- Даем права на схемы
GRANT ALL ON SCHEMA public TO appuser;
