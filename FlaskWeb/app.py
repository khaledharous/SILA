from flask import Flask, render_template

app = Flask(__name__, template_folder="SILA")

@app.route('/')
def index():
    return "Welcome to SILA"

@app.route('/signup')
def signup():
    return render_template('signup/templates/signup.html')

@app.route('/login')
def login():
    return render_template('login/templates/login.html')

@app.route('/forgotpassword')
def forgotpassword():
    return render_template('forgotpassword/templates/forgotpassword.html')

if __name__ == '__main__':
    app.run(debug=True)
