from flask import Flask, render_template, request, redirect, url_for, g
import sqlite3

app = Flask(__name__)

def get_conn():
    if 'conn' not in g:
        g.conn = sqlite3.connect('shopping_list.db')
    return g.conn

def create_table():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT, date TEXT, status TEXT)")

@app.route('/')
def home():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    return render_template('home.html', list=rows)

@app.route('/add', methods=['POST'])
def add():
    conn = get_conn()
    cursor = conn.cursor()
    task = request.form['task']
    date = request.form['date']
    cursor.execute("INSERT INTO tasks (task, date) VALUES (?, ?)", (task, date))
    conn.commit()
    return redirect(url_for('home'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_conn()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        status = request.form['status']
        cursor.execute("UPDATE tasks SET task=?, date=?, status=? WHERE id=?", (name, date, status, id))
        conn.commit()
        return redirect(url_for('home'))
    else:
        cursor.execute("SELECT * FROM tasks WHERE id=?", (id,))
        task = cursor.fetchone()
        return render_template('edit.html', task=task)
    
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        create_table()
        conn = get_conn()
    app.run(port=5000)