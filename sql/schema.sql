CREATE DATABASE taskmanager;

USE taskmanager;

CREATE TABLE users(
    id INT AUTO_INCREMENT PRIMARY KEY,
    fullname VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE tasks(
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    title VARCHAR(100),
    description TEXT,
    priority VARCHAR(20),
    status VARCHAR(20),
    due_date DATE,
    FOREIGN KEY(user_id) REFERENCES users(id)
);