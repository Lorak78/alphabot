import socket
import time

MY_ADDRESS = ("10.210.0.93", 9090)
BUFFER_SIZE = 4096
TIMEOUT = 10  # 10 secondi di timeout per considerare il client disconnesso

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    
    connection, client_address = s.accept()  # bloccante
    print(f"Il client {client_address} si è connesso")

    last_message_time = time.time()  # Tenere traccia dell'ultimo messaggio ricevuto

    while True:
        # Imposta un timeout per la connessione
        connection.settimeout(1)

        try:
            message = connection.recv(BUFFER_SIZE)
            if not message:
                print("Connessione Interrotta")
                break  # Il client si è disconnesso

            direz_decode = message.decode()
            last_message_time = time.time()  # Aggiorna il tempo dell'ultimo messaggio

            if direz_decode == "KEEP-ALIVE":
                print("Keep-alive ricevuto dal client")
                continue  # Ignora il keep-alive, ma aggiorna il timer

            diz_movimenti = eval(direz_decode)  # Trasforma l'fstring in dizionario

            # Esegui le operazioni in base ai comandi ricevuti
            if diz_movimenti["w"]:
                if diz_movimenti["a"]:
                    print("avanti sinistra")
                elif diz_movimenti["d"]:
                    print("avanti destra")
                else:
                    print("avanti")
            elif diz_movimenti["s"]:
                if diz_movimenti["a"]:
                    print("indietro sinistra")
                elif diz_movimenti["d"]:
                    print("indietro destra")
                else:
                    print("indietro")
            elif diz_movimenti["a"]:
                print("sinistra")
            elif diz_movimenti["d"]:
                print("destra")
            elif all(not valore for valore in diz_movimenti.values()):
                print("stop")

        except socket.timeout:
            # Controlla se è passato troppo tempo dall'ultimo messaggio
            if time.time() - last_message_time > TIMEOUT:
                print("Timeout: client non ha inviato dati, considerato disconnesso.")
                break

    connection.close()

if __name__ == "__main__":
    main()
