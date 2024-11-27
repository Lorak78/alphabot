import sqlite3

conn = sqlite3.connect("comandi.db")
cur = conn.cursor()

cur.execute('''insert into tabellaComandi (tasto_movimento, str_azione)
            values ("q", "f100,l20,f40"),
            ("e", "l50,f100,r50"),
            ("r", "b50,r50,f20"),
            ("f", "r50,f100,l50");''')
conn.commit()
variabile_in_stampa = cur.fetchall()