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
            section TEXT NOT NULL,
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
    student_id = request.form.get('studentid', '').strip()
    section = request.form.get('section', '')
    address = request.form.get('address', '')
    email = request.form.get('email', '').strip()
    city = request.form.get('city', '')
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm-password', '')

    if not re.match(r"^\d{8,12}$", student_id):
        flash("Error: Student ID must be between 8-12 digits and contain only numbers!", "error")
        return redirect(url_for('person'))

    if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
        flash("Invalid email format!", "error")
        return redirect(url_for('person'))
    
    if password != confirm_password:
        flash("Error: Passwords do not match!", "error")
        return redirect(url_for('person'))
    
    if len(password) < 8:
        flash("Error: Password must be at least 8 characters long !", "error")
        return redirect(url_for('person'))
    
    hashed_password = generate_password_hash(password)
    
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        
        
        cursor.execute("SELECT * FROM users WHERE student_id = ?", (student_id,))
        existing_student = cursor.fetchone()
        if existing_student:
            flash("Error: Student ID already exists !", "error")
            conn.close()
            return redirect(url_for('person'))
        
    
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_email = cursor.fetchone()
        if existing_email:
            flash("Error: Email already exists!", "error")
            conn.close()
            return redirect(url_for('person'))

       
        cursor.execute("INSERT INTO users (username, student_id, section, address, email, city, password) VALUES (?, ?, ?, ?, ?, ?, ?)", 
                       (username, student_id, section, address, email, city, hashed_password))
        conn.commit()
    finally:
        conn.close()
    
    flash("Registration successful! Please Sign In", "success")
    return redirect(url_for('person'))

# Login Route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[7], password):  # Verify password
            # Store user data in session
            session["user"] = {
                "id": user[0],
                "username": user[1],
                "student_id": user[2],
                "section": user[3],
                "address": user[4],
                "email": user[5],
                "city": user[6]
            }

            flash("Login successful!", "success")
            return redirect(url_for("profile"))  # Redirect to profile page
        else:
            flash("Invalid username or password. Please Signup if you dont have an account", "error")

    return render_template("login.html")


# Profile Route
@app.route("/profile")
def profile():
    if "user" not in session:
        flash("Please log in first!", "error")
        return redirect(url_for("login"))
    
    # Retrieve user data from session
    user_data = session["user"]
    return render_template("profile.html", user=user_data)
@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("login"))

# Forgot Password Route
@app.route("/forgotpassword", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form["email"].strip()
        if email_exists(email):
            if send_reset_email(email):flash("A password reset link has been sent to your email.", "success")
            else:
                flash("Failed to send email. Try again later.", "error")
        else:
            flash("Email not found in the system.", "error")
    return render_template("forgotpassword.html")

# Reset Password Route
@app.route("/resetpassword", methods=["GET", "POST"])
def reset_password():
    email = request.args.get("email","")
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

# Helper Functions
def send_reset_email(user_email):
    reset_link = f"http://127.0.0.1:5000/resetpassword?email={user_email}"
    subject = "Password Reset Request"
    body = f"Click the link below to reset your password:\n\n{reset_link}"

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "your_email@yandex.com"
    msg["To"] = user_email

    try:
        server = smtplib.SMTP("smtp.yandex.com", 587)
        server.starttls()
        server.login("your_email@yandex.com", "your_email_password")
        server.sendmail("your_email@yandex.com", user_email, msg.as_string())
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

@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/person")
def person():
    return render_template("person.html")

if __name__== "__main__":
    app.run(debug=True)