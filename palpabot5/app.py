from flask import Flask, render_template, request
import AlphaBot
app = Flask(__name__)
alphaBot = AlphaBot.AlphaBot()

@app.route("/", methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        print(request.form.get('action1'))
        if request.form.get('w') == 'value1':
            alphaBot.setMotor(-43, 47)
        elif  request.form.get('s') == 'value2':
            alphaBot.setMotor(43, -47)
        if request.form.get('a') == 'value3':
            alphaBot.left()
        elif  request.form.get('d') == 'value4':
            alphaBot.right()
        else:
            print("Unknown")
    elif request.method == 'GET':
        return render_template('index.html')
    
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True, host='localhost')