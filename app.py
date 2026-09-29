from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Функция для создания подключения к базе данных
def get_db_connection():
    conn = sqlite3.connect('journal.db')
    conn.row_factory = sqlite3.Row  # Позволяет обращаться к колонкам по их именам
    return conn

# Инициализация базы данных: создаем таблицу, если её ещё нет
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            task TEXT NOT NULL,
            hours INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Запускаем инициализацию при старте приложения
init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    # Запрашиваем все записи из базы данных, сортируя от новых к старым
    entries = conn.execute('SELECT * FROM entries ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    task = request.form.get('task')
    hours = request.form.get('hours')
    
    if task and hours:
        current_date = datetime.today().strftime('%Y-%m-%d')
        
        conn = get_db_connection()
        # Безопасно вставляем данные пользователя в таблицу entries
        conn.execute('INSERT INTO entries (date, task, hours) VALUES (?, ?, ?)',
                     (current_date, task, int(hours)))
        conn.commit()
        conn.close()
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Используем порт 8080, чтобы точно обойти системные блокировки портов Windows
    app.run(debug=True, port=8080)
