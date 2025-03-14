from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import smtplib
import re
from werkzeug.security import generate_password_hash, check_password_hash
from email.mime.text import MIMEText

app = Flask(__name__, template_folder="SILA/templates", static_folder="SILA/static")
app.secret_key = "your_secret_key"

# Database Initialization
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
    username = request.form.get('username', '')
    student_id = request.form.get('studentid', '')
    address = request.form.get('address', '')
    email = request.form.get('email', '').strip()
    city = request.form.get('city', '')
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm-password', '')

    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        flash("Invalid email format!", "error")
        return redirect(url_for('person'))
    
    if password != confirm_password:
        flash("Error: Passwords do not match!", "error")
        return redirect(url_for('person'))
    
    hashed_password = generate_password_hash(password)
    
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, student_id, address, email, city, password) VALUES (?, ?, ?, ?, ?, ?)", 
                       (username, student_id, address, email, city, hashed_password))
        conn.commit()
    except sqlite3.IntegrityError:
        flash("Error: Email already exists!", "error")
        return redirect(url_for('person'))
    finally:
        conn.close()
    
    flash("Registration successful!", "success")
    return redirect(url_for('person'))

# Email settings
SMTP_SERVER = "smtp.yandex.com"
SMTP_PORT = 587
EMAIL_SENDER = "your_email@yandex.com"
EMAIL_PASSWORD = "your_email_password"

def send_reset_email(user_email):
    reset_link = f"http://127.0.0.1:5000/resetpassword?email={user_email}"
    subject = "Password Reset Request"
    body = f"Click the link below to reset your password:\n\n{reset_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = user_email

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, user_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def email_exists(email):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user is not None

@app.route("/forgotpassword", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"].strip()
        if email_exists(email):
            if send_reset_email(email):
                flash("A password reset link has been sent to your email.", "success")
            else:
                flash("Failed to send email. Try again later.", "error")
        else:
            flash("Email not found in the system.", "error")
    return render_template("forgotpassword.html")

@app.route("/resetpassword", methods=["GET", "POST"])
def reset_password():
    email = request.args.get("email", "")
    if request.method == "POST":
        new_password = request.form["new_password"]
        hashed_password = generate_password_hash(new_password)
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (hashed_password, email))
        conn.commit()
        conn.close()
        flash("Your password has been updated!", "success")
        return redirect(url_for("login"))
    return render_template("resetpassword.html", email=email)

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/person")
def person():
    return render_template("person.html")    

@app.route("/profile")
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.run(debug=True)