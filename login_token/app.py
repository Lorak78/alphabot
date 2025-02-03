from flask import Flask, render_template, redirect, url_for, request, make_response
import sqlite3
import jwt, datetime

app = Flask(__name__)
SECRET_KEY = "mysecretkey"

def validate(username, password):
    completion = False
    con = sqlite3.connect('./comandi.db')
    cur = con.cursor()
    cur.execute("SELECT * FROM tabellaLogin")
    rows = cur.fetchall()
    for row in rows:
        dbUser = row[1]
        dbPass = row[2]
        if dbUser == username:
            completion = check_password(dbPass, password)
    return completion

def check_password(hashed_password, user_password):
    return hashed_password == user_password

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        conn = sqlite3.connect("comandi.db")
        cur = conn.cursor()
        username = request.form['e-mail']
        password = request.form['password']
        cur.execute('''INSERT INTO tabellaLogin (username, password) VALUES (?, ?);''', (username, password))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('create_account.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['e-mail']
        password = request.form['password']
        completion = validate(username, password)
        if not completion:
            error = 'Invalid Credentials. Please try again.'
        else:
            expiration = datetime.datetime.utcnow() + datetime.timedelta(days=1)
            token = jwt.encode({"username": username, "exp": expiration}, SECRET_KEY, algorithm="HS256")
            response = make_response(redirect(url_for('index')))
            response.set_cookie("token", token, max_age=60 * 60 * 24, httponly=True)
            return response
    return render_template('login.html', error=error)

@app.route("/index", methods=['GET', 'POST'])
def index():
    token = request.cookies.get("token")
    if token:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            username = decoded_token.get("username", username)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login"))
    
    if request.method == 'POST':
        if request.form.get('logout') == "logout":
            return redirect(url_for("logout"))
    return render_template("index.html", username=username)

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie("token")
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    token = request.cookies.get("token")
    if token:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return redirect(url_for("index"))
        except jwt.ExpiredSignatureError:
            return redirect(url_for("login"))
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
