from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__, template_folder="SILA/templates", static_folder="SILA/static")
app.secret_key = "your_secret_key"


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
@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    student_id = request.form['studentid']
    address = request.form['address']
    email = request.form['email']
    city = request.form['city']
    password = request.form['password']
    confirm_password = request.form['confirm-password']

    
    if password != confirm_password:
        flash("Error: Passwords do not match!", "error")
        return redirect(url_for('person'))

    
    masked_password = '*' * len(password)

    
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, student_id, address, email, city, password) VALUES (?, ?, ?, ?, ?, ?)", 
                       (username, student_id, address, email, city, masked_password))
        conn.commit()
        conn.close()
        flash("Registration successful!", "success")
        return redirect(url_for('person'))
    except sqlite3.IntegrityError:
        flash("Error: Email already exists!", "error")
        return redirect(url_for('person'))

# إعدادات البريد الإلكتروني عبر Yandex
SMTP_SERVER = "smtp.yandex.com"
SMTP_PORT = 465
EMAIL_SENDER = "your_email@yandex.com"
EMAIL_PASSWORD = "your_email_password"

# وظيفة إرسال الإيميل
def send_reset_email(user_email):
    reset_link = f"http://127.0.0.1:5000/resetpassword?email={user_email}"
    subject = "Password Reset Request"
    body = f"Click the link below to reset your password:\n\n{reset_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = user_email

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, user_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

# دالة للتحقق من وجود البريد في قاعدة البيانات
def email_exists(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

# **🔹 مسار صفحة "نسيت كلمة السر"**
@app.route("/forgotpassword", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"]
        if email_exists(email):
            if send_reset_email(email):
                flash("A password reset link has been sent to your email.", "success")
            else:
                flash("Failed to send email. Try again later.", "error")
        else:
            flash("Email not found in the system.", "error")
    return render_template("forgotpassword.html")


@app.route("/")
def login():
    return render_template("login.html")

@app.route("/person")
def person():
    return render_template("person.html")    

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/forgotpassword")
def forgotpassword():
    return render_template("forgotpassword.html")

if __name__ == "__main__":
    app.run(debug=True)