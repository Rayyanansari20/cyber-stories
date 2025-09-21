from flask import Flask, render_template, request, redirect, session
import sqlite3
import requests

app = Flask(__name__)
app.secret_key = "supersecretkey"

conn = sqlite3.connect('database.db', check_same_thread=False)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, email TEXT, password TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS posts(id INTEGER PRIMARY KEY, user TEXT, story TEXT, link TEXT)''')
conn.commit()

@app.route('/')
def index():
    c.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = c.fetchall()
    return render_template('index.html', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        c.execute("INSERT INTO users(email,password) VALUES(?,?)", (email, password))
        conn.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=='POST':
        email = request.form['email']
        password = request.form['password']
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email,password))
        user = c.fetchone()
        if user:
            session['user'] = email
            return redirect('/')
        else:
            return "Invalid credentials"
    return render_template('login.html')

@app.route('/post', methods=['GET','POST'])
def post_story():
    if 'user' not in session:
        return redirect('/login')
    if request.method=='POST':
        story = request.form['story']
        link = request.form['link']
        if link:
            try:
                r = requests.get(link, timeout=3)
                if r.status_code != 200:
                    link = "⚠ Possibly Fake Link"
            except:
                link = "⚠ Possibly Fake Link"
        c.execute("INSERT INTO posts(user,story,link) VALUES(?,?,?)", (session['user'],story,link))
        conn.commit()
        return redirect('/')
    return render_template('post.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)