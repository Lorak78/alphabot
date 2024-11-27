import sqlite3

conn = sqlite3.connect("comandi.db")
cur = conn.cursor()

cur.execute('''CREATE TABLE "tabellaComandi"(
                "tasto_movimento" VARCHAR(1),
                "str_azione" TEXT NOT NULL,
                PRIMARY KEY("tasto_movimento")
            );''')
conn.commit()
variabile_in_stampa = cur.fetchall()