import socket
import time
import AlphaBot
import sqlite3

MY_ADDRESS = ("10.210.0.138", 9090)
BUFFER_SIZE = 4096
TIMEOUT = 10

alphaBot = AlphaBot.AlphaBot()

conn = sqlite3.connect("comandi.db")
cur = conn.cursor()

dati_tabella = cur.execute("SELECT * FROM tabellaComandi")
lista_tabella = dati_tabella.fetchall()

diz_comandi_tabella = {elem[0]:elem[1] for elem in lista_tabella}

def main():
    alphaBot.stop()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    
    connection, client_address = s.accept()  #bloccante
    print(f"Il client {client_address} si è connesso")

    last_message_time = time.time()

    while True:
        connection.settimeout(1)

        try:
            message = connection.recv(BUFFER_SIZE)
            if not message:
                print("Connessione Interrotta")
                alphaBot.stop()
                break 

            direz_decode = message.decode()
            last_message_time = time.time()

            if direz_decode == "KEEP-ALIVE":
                print("Keep-alive ricevuto dal client")
                continue

            diz_movimenti = eval(direz_decode)

            if diz_movimenti["w"]:
                print("avanti")
                alphaBot.forward()
            elif diz_movimenti["s"]:
                print("indietro")
                alphaBot.backward()
            elif diz_movimenti["a"]:
                print("sinistra")
                alphaBot.left()
            elif diz_movimenti["d"]:
                print("destra")
                alphaBot.right()
            elif all(not valore for valore in diz_movimenti.values()):
                print("stop")
                alphaBot.stop()
            

        except socket.timeout:
            if time.time() - last_message_time > TIMEOUT:
                print("Timeout: client non ha inviato dati, considerato disconnesso.")
                alphaBot.stop()
                break
        if direz_decode not in diz_comandi_tabella:
            alphaBot.stop()
        else:
            print(diz_comandi_tabella[direz_decode])

    connection.close()

if __name__ == "__main__":
    main()
