import sqlite3

conn = sqlite3.connect("comandi.db")
cur = conn.cursor()

variabile_in_stampa = cur.execute("SELECT * FROM tabellaComandi")
lista_tabella = variabile_in_stampa.fetchall()

a = {el[0]:el[1] for el in lista_tabella}
print(a)