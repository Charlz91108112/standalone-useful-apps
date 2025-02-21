from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure key in production

def get_db_connection():
    conn = sqlite3.connect('expense.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        # Drop existing tables to start fresh with updated schema
        conn.execute("DROP TABLE IF EXISTS users")
        conn.execute("DROP TABLE IF EXISTS expenses")
        conn.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """)
        conn.execute("""
        CREATE TABLE expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            currency TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        """)
    conn.close()

@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    conn = get_db_connection()
    if start_date and end_date:
        expenses = conn.execute('SELECT * FROM expenses WHERE user_id = ? AND date BETWEEN ? AND ?', (session['user_id'], start_date, end_date)).fetchall()
    else:
        expenses = conn.execute('SELECT * FROM expenses WHERE user_id = ?', (session['user_id'],)).fetchall()
    # Compute chart data by aggregating expenses by date
    chart_data = {}
    for expense in expenses:
        dt = expense['date']
        chart_data[dt] = chart_data.get(dt, 0) + expense['amount']
    labels = sorted(chart_data.keys())
    values = [chart_data[dt] for dt in labels]
    conn.close()
    return render_template('dashboard.html', expenses=expenses, chart_labels=labels, chart_values=values)

@app.route('/add', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('sign_in'))
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount')
        date = request.form.get('date')
        currency = request.form.get('currency', 'AED')
        conn = get_db_connection()
        conn.execute('INSERT INTO expenses (user_id, category, amount, date, currency) VALUES (?, ?, ?, ?, ?)',
                     (session['user_id'], category, amount, date, currency))
        conn.commit()
        conn.close()
        return redirect(url_for('dashboard'))
    return render_template('add_expense.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match!')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password)
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_password))
            conn.commit()
        except sqlite3.IntegrityError:
            flash('Username already exists!')
            conn.close()
            return redirect(url_for('register'))
        conn.close()
        flash('Registered successfully! Please sign in.')
        return redirect(url_for('sign_in'))
    return render_template('register.html')

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        conn.close()
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials!')
            return redirect(url_for('sign_in'))
    return render_template('signin.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('sign_in'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host="0.0.0.0", port=4000)
