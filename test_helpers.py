from flask import Flask, request, render_template_string, redirect
import sqlite3
import subprocess
import requests

app = Flask(__name__)

# --- Initialize SQLite Database ---
def init_db():
    conn = sqlite3.connect('vulnlab.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            bio TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- Home Route ---

app = Flask(__name__)

# --- Initialize SQLite Database ---
def init_db():
    conn = sqlite3.connect('vulnlab.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            bio TEXT
        )@app.route('/')
def home():
    return '''
        <h1>Welcome to the Vulnerable Lab</h1>
        <ul>
            <li><a href="/register">Register (SQLi)</a></li>
            <li><a href="/login">Login (SQLi)</a></li>
            <li><a href="/profile?user=test">View Profile (XSS)</a></li>
            <li><a href="/exec">Execute Command (RCE)</a></li>
            <li><a href="/ssrf?url=http://example.com">Fetch External URL (SSRF)</a></li>
        </ul>
    '''

# --- Registration Page (SQLi) ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        bio = request.form.get('bio', 'No bio')

        conn = sqlite3.connect('vulnlab.db')
        cur = conn.cursor()

        # 🚨 SQL Injection vulnerability
        query = f"INSERT INTO users (username, password, bio) VALUES ('{username}', '{password}', '{bio}')"
        cur.execute(query)
        conn.commit()
        conn.close()

        return "Registered successfully!"
    
    return '''
        <h2>Register</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            Bio: <textarea name="bio"></textarea><br>

app = Flask(__name__)

# --- Initialize SQLite Database ---
def init_db():
    conn = sqlite3.connect('vulnlab.db')
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            password TEXT,
            bio TEXT
        )         
<input type="submit" value="Register">
        </form>
    '''

# --- Login Page (SQLi) ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('username')
        passwd = request.form.get('password')

        conn = sqlite3.connect('vulnlab.db')
        cur = conn.cursor()

        # 🚨 SQL Injection vulnerability
        sql = f"SELECT * FROM users WHERE username = '{uname}' AND password = '{passwd}'"
        cur.execute(sql)
        user = cur.fetchone()
        conn.close()

        if user:
            return f"<h3>Welcome {uname}</h3>"
        else:
            return "Invalid credentials"
    
    return '''
        <h2>Login</h2>
        <form method="POST">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

# --- Profile Page (XSS) ---
@app.route('/profile')
def profile():
    username = request.args.get('user', '')
    conn = sqlite3.connect('vulnlab.db')
    cur = conn.cursor()
    cur.execute(f"SELECT bio FROM users WHERE username = '{username}'")
    row = cur.fetchone()
    conn.close()

    bio = row[0] if row else "No bio available"
    # 🚨 XSS vulnerability
    return render_template_string(f"<h2>Profile of {username}</h2><p>Bio: {bio}</p>")

# --- RCE (Remote Command Execution) ---
@app.route('/exec', methods=['GET', 'POST'])
def exec_cmd():
    if request.method == 'POST':
        command = request.form.get('cmd')
        try:
            # 🚨 RCE vulnerability
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, timeout=5)
            return f"<pre>{result.decode()}</pre>"
        except Exception as e:
            return f"<pre>Error: {e}</pre>"
    
    return '''
        <h2>Execute Command</h2>
        <form method="POST">
            Command: <input name="cmd"><br>
            <input type="submit" value="Run">
        </form>
    '''

# --- SSRF (Server-Side Request Forgery) ---
@app.route('/ssrf')
def ssrf():
    url = request.args.get('url')
    try:
        # 🚨 SSRF vulnerability
        resp = requests.get(url, timeout=5)
        return f"<pre>{resp.text}</pre>"
    except Exception as e:
        return f"<pre>Failed to fetch URL: {e}</pre>"

# --- Start App ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
