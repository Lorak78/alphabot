from flask import Flask, render_template #render_template prende un file html come parametro e crea un oggetto

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cakes')
def cakes():
    return 'Yummy cakes!'

@app.route('/hello/<name>') #URL dinamica <name> è un campo variabile
def hello(name):
    return render_template('page.html', name_html=name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')