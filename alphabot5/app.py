from flask import Flask, render_template, request
import AlphaBot
app = Flask(__name__)
alphaBot = AlphaBot.AlphaBot()
alphaBot.stop()

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.form.get('action1'))
        if request.form.get('w') == 'avanti':
            alphaBot.setMotor(-43, 47)
        elif  request.form.get('s') == 'indietro':
            alphaBot.setMotor(43, -47)
        elif request.form.get('a') == 'sinistra':
            alphaBot.left()
        elif  request.form.get('d') == 'destra':
            alphaBot.right()
        elif request.form.get('stop') == 'stop':
            alphaBot.stop()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.129')