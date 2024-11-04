import socket
import time
import AlphaBot
import sqlite3

MY_ADDRESS = ("192.168.1.128", 9090)
BUFFER_SIZE = 4096
TIMEOUT = 10

alphaBot = AlphaBot.AlphaBot()

conn = sqlite3.connect("comandi.db")
cur = conn.cursor()

dati_tabella = cur.execute("SELECT * FROM tabellaComandi")
lista_tabella = dati_tabella.fetchall()

diz_comandi_tabella = {elem[0]:elem[1] for elem in lista_tabella}

def controlloInDizTabella(diz_movimenti):
    for key in diz_movimenti:
        if key in diz_comandi_tabella and diz_movimenti[key]:
            return key
    return ""  

def eseguiComandoTabella(str_comandi:str):
    lista_comandi = str_comandi.split(",")
    #print(lista_comando)
    for comando in lista_comandi:
        time.sleep(0.7)
        if comando[0] == "f":
            print(f"avanti,{int(comando[1:])}")
            alphaBot.forward()
            time.sleep(int(comando[1:])/100)
            alphaBot.stop()
        elif comando[0] == "b":
            print(f"indietro,{int(comando[1:])}")
            alphaBot.backward()
            time.sleep(int(comando[1:])/100)
            alphaBot.stop()
        elif comando[0] == "l":
            print(f"sinistra,{int(comando[1:])}")
            alphaBot.left()
            time.sleep(int(comando[1:])/100)
            alphaBot.stop()
        elif comando[0] == "r":
            print(f"destra,{int(comando[1:])}")
            alphaBot.right()
            time.sleep(int(comando[1:])/100)
            alphaBot.stop()
    
def main():
    alphaBot.stop()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    
    connection, client_address = s.accept()  #bloccante
    print(f"Il client {client_address} si è connesso")
    print(f"diz comandi: {diz_comandi_tabella}")

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

            if "KEEP-ALIVE" in direz_decode or "}{" in direz_decode:
                print("Keep-alive ricevuto dal client")
                continue

            diz_movimenti = eval(direz_decode)
            print(diz_movimenti)
            lettera = controlloInDizTabella(diz_movimenti)
            print(lettera)

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
            elif lettera != "":
                eseguiComandoTabella(diz_comandi_tabella[lettera])
            else:
                alphaBot.stop()

        except socket.timeout:
            if time.time() - last_message_time > TIMEOUT:
                print("Timeout: client non ha inviato dati, considerato disconnesso.")
                alphaBot.stop()
                break

    connection.close()

if __name__ == "__main__":
    main()
