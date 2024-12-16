from flask import Flask

#gestisce tutto non dobbiamo usare thread

app = Flask(__name__)

@app.route('/') #mappata sulla route
def index():
    return 'Ciao!'

@app.route('/pagina/') #mappa la funzione index2 sulla route /pagina
def index2():
    return 'pagina!'

if __name__ == '__main__':
    app.run(debug=True, host='localhost') #debug=True permette di modificare il codice mentre il codice è in esecuzione senza dover rieseguire il codice