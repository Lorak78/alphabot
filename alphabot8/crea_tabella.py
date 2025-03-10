import sqlite3

conn = sqlite3.connect("./comandi.db")
cur = conn.cursor()

cur.execute('''CREATE TABLE "tabellaLogin"(
                "id" INTEGER,
                "username" VARCHAR(25),
                "password" VARCHAR(10) NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT)
            );''')
conn.commit()
variabile_in_stampa = cur.fetchall()