-- V1__create_users_table.sql
-- Создание таблицы users

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100),
    password_user VARCHAR(100),
    payment BOOLEAN DEFAULT FALSE,
    id_tg BIGINT UNIQUE,
    tg_name varchar(100)

);