# Task Manager (Flask + MySQL)

A Task Manager web application built using Flask and MySQL.for #Live demo https://task-manager-de.onrender.com

## Features

- User Registration
- Secure Login
- Password Hashing (bcrypt)
- Dashboard
- Add Task
- Edit Task
- Delete Task
- Search Tasks
- Task Statistics
- Session Authentication

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript
- bcrypt

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/deepak-deve/task-manager-project.git

cd task-manager-project
```

## 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Create the MySQL database

Open MySQL and run the SQL script located in:

```text
sql/schema.sql
```

or

```sql
SOURCE sql/schema.sql;
```

This will create the required database and tables.

## 5. Configure the database

Open:

```text
database/db.py
```

Update these values:

```python
host="localhost"
user="root"
password="your_password"
database="taskmanager"
```

## 6. Run the application

```bash
python app.py
```

Open your browser and visit:

```
http://127.0.0.1:5000
```

## Project Structure

```
TaskManager/
│
├── app.py
├── requirements.txt
├── database/
├── routes/
├── static/
├── templates/
└── sql/
```

## Author

Deepakraj K
