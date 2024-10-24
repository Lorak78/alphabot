import sqlite3

conn = sqlite3.connect("comandi.db")
cur = conn.cursor()

variabile_in_stampa = cur.execute("SELECT * FROM tabellaComandi")
print(variabile_in_stampa.fetchall())