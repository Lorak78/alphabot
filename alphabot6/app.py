from flask import Flask, render_template, redirect, url_for, request, make_response
import sqlite3
import AlphaBot

app = Flask(__name__)
alphaBot = AlphaBot.AlphaBot()
alphaBot.stop()

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
        cur.execute('''INSERT INTO tabellaLogin (username, password)
                       VALUES (?, ?);''', (username, password))
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
            response = make_response(redirect(url_for('index')))
            response.set_cookie("username", username, max_age=60 * 60 * 24)
            return response
    return render_template('login.html', error=error)

@app.route("/index", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if request.form.get('logout') == "logout":
            return redirect(url_for("logout"))
        elif request.form.get('esc') == "esc":
            return redirect(url_for("login"))
        elif request.form.get('w') == 'avanti':
            print("avanti")
            alphaBot.setMotor(-43, 47)
        elif request.form.get('s') == 'indietro':
            print("indietro")
            alphaBot.setMotor(43, -47)
        elif request.form.get('a') == 'sinistra':
            print("sinistra")
            alphaBot.left()
        elif request.form.get('d') == 'destra':
            print("destra")
            alphaBot.right()
        elif request.form.get('stop') == 'stop':
            print("stop")
            alphaBot.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    return render_template("index.html")

@app.route('/logout')
def logout():
    response = make_response(redirect(url_for('login')))
    response.delete_cookie("username")
    return response

@app.route('/', methods=['GET', 'POST'])
def home():
    username = request.cookies.get("username")
    if not username:
        return redirect(url_for("login"))
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.129')