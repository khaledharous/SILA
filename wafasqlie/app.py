from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# إنشاء قاعدة البيانات إذا لم تكن موجودة
conn = sqlite3.connect('users.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        studentid TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        address TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        city TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

@app.route('/')
def home():
    return render_template('signup.html')

@app.route('/signup', methods=['POST'])
def signup():
    studentid = request.form['studentid']
    username = request.form['username']
    address = request.form['address']
    email = request.form['email']
    city = request.form['city']
    password = request.form['password']

    try:
        cursor.execute("INSERT INTO users (studentid, username, address, email, city, password) VALUES (?, ?, ?, ?, ?, ?)", 
                       (studentid, username, address, email, city, password))
        conn.commit()
        return "Registration Successful!"
    except sqlite3.IntegrityError:
        return "Error: Student ID or Email already exists!"

if __name__ == '__main__':
    app.run(debug=True)
