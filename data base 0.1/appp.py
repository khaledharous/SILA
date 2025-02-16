from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"  # مفتاح سري لاستخدام flash messages

# إنشاء قاعدة البيانات والجدول
def create_database():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            student_id TEXT NOT NULL,
            address TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            city TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

# عرض صفحة التسجيل
@app.route('/signup')
def signup():
    return render_template('signup.html')

# معالجة تسجيل المستخدم
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    student_id = request.form['studentid']
    address = request.form['address']
    email = request.form['email']
    city = request.form['city']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    # التحقق من أن كلمة المرور متطابقة
    if password != confirm_password:
        flash("Error: Passwords do not match!", "error")
        return redirect(url_for('signup'))

    # إدخال البيانات إلى قاعدة البيانات
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, student_id, address, email, city, password) VALUES (?, ?, ?, ?, ?, ?)", 
                       (username, student_id, address, email, city, password))
        conn.commit()
        conn.close()
        flash("Registration successful!", "success")
        return redirect(url_for('signup'))
    except sqlite3.IntegrityError:
        flash("Error: Email already exists!", "error")
        return redirect(url_for('signup'))

if __name__ == '__main__':
    app.run(debug=True)