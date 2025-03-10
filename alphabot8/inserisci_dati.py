import sqlite3

conn = sqlite3.connect("comandi.db")
cur = conn.cursor()

cur.execute('''insert into tabellaLogin (username, password)
            values ("simone", "12345"),
            ("karol", "ciao1"),
            ("mario", "mario10"),
            ("paolo", "ciao2");''')
conn.commit()
variabile_in_stampa = cur.fetchall()