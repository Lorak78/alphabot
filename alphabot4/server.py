import socket
import time # serve per la gestione della caduta della connessione con il keep-alive
import AlphaBot
import sqlite3

MY_ADDRESS = ("192.168.1.129", 9090)
BUFFER_SIZE = 4096
TIMEOUT = 10 #in secondi, tempo che si attende senza ricevere il keep-alive prima di arrestare il programma

alphaBot = AlphaBot.AlphaBot() #Creazione alphabot

conn = sqlite3.connect("./../comandi.db") #associazione di una variabile alla tabella comandi
cur = conn.cursor() # serve per eseguire le query

dati_tabella = cur.execute("SELECT * FROM tabellaComandi")
lista_tabella = dati_tabella.fetchall() # memorizzazione della select in una variabile

diz_comandi_tabella = {elem[0]:elem[1] for elem in lista_tabella} # una volta letta la tabella, associo la lettera (chiave) alla stringa del comando (valore)

def controlloInDizTabella(diz_movimenti):
    """
    Controlla se esiste una chiave in `diz_movimenti` che sia presente anche in `diz_comandi_tabella` 
    e il cui valore in `diz_movimenti` sia True.

    Parametri:
    ----------
    diz_movimenti : dict
        Un dizionario in cui le chiavi rappresentano movimenti o comandi e i valori 
        indicano se il movimento è attivo (True) o non attivo (False).
    
    Ritorna:
    --------
    str
        La prima chiave trovata che è presente sia in `diz_movimenti` sia in `diz_comandi_tabella`
        con valore True in `diz_movimenti`. Se nessuna chiave soddisfa questa condizione, 
        restituisce una stringa vuota ("").
    
    Esempio:
    --------
    >>> diz_movimenti = {"salta": True, "corri": False, "spara": True}
    >>> diz_comandi_tabella = {"salta": "jump", "cammina": "walk", "spara": "shoot"}
    >>> controlloInDizTabella(diz_movimenti)
    'salta'
    """
    for key in diz_movimenti:
        if key in diz_comandi_tabella and diz_movimenti[key]:
            return key
    return ""  

def eseguiComandoTabella(str_comandi:str):

    """
    Esegue una serie di comandi di movimento per un robot AlphaBot in base a una stringa di input formattata. 
    I comandi specificano direzioni e durate per ogni movimento del robot.

    Parametri:
    ----------
    str_comandi : str
        Una stringa contenente comandi separati da virgola, dove ciascun comando è costituito da:
        - una lettera per la direzione ('f' per avanti, 'b' per indietro, 'l' per sinistra, 'r' per destra)
        - una cifra o un numero che indica la durata del movimento, un valore diviso poi per 100 che e' la durata in secondi.
    
    Funzionamento:
    --------------
    La funzione divide `str_comandi` in una lista di singoli comandi e li esegue uno alla volta. Per ciascun comando:
    - Attende 0.7 secondi prima di procedere.
    - Interpreta la lettera iniziale per stabilire la direzione.
    - Esegue il movimento per la durata specificata (valore diviso poi per 100).
    - Ferma il movimento del robot dopo il tempo specificato.
    
    Ogni movimento è eseguito utilizzando i metodi del robot AlphaBot (`forward`, `backward`, `left`, `right`), 
    e la funzione `stop` è chiamata per interrompere il movimento al termine del tempo specificato.

    Esempio:
    --------
    >>> eseguiComandoTabella("f50,b30,l20,r40")
    avanti,50
    indietro,30
    sinistra,20
    destra,40

    Questo esempio invia i seguenti comandi al robot AlphaBot:
    - Avanza per 0.5 secondi.
    - Va indietro per 0.3 secondi.
    - Ruota a sinistra per 0.2 secondi.
    - Ruota a destra per 0.4 secondi.
    
    Notare:
    -------
    Alphabot e' una libreria importata
    """

    lista_comandi = str_comandi.split(",")
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
    alphaBot.stop() #arresto dell'alphabot all'inizio del programma

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creazione socket tcp
    s.bind(MY_ADDRESS) #associazione del server all'indirizzo
    s.listen()
    
    connection, client_address = s.accept()  #bloccante, si sblocca quando si connette il client
    print(f"Il client {client_address} si è connesso")
    print(f"diz comandi: {diz_comandi_tabella}")

    last_message_time = time.time() # tempo trascorso dall'ultimo messaggio ricevuto

    while True:
        connection.settimeout(1)#serve a impostare un timeout di 1 secondo per le operazioni di ricezione dei messaggi dal client 

        try:
            message = connection.recv(BUFFER_SIZE) #riceve il messaggio
            if not message:#se il messaggio è vuoto
                print("Connessione Interrotta") #vuol dire che la connessione è interrotta
                alphaBot.stop() # fermo l'alphabot
                break #esco dal while true

            direz_decode = message.decode() # decodifica messagio
            last_message_time = time.time() # riaggiornamento dell'ultimo messaggio ricevuto

            if "KEEP-ALIVE" in direz_decode or "}{" in direz_decode:
                print("Keep-alive ricevuto dal client")
                #se il messaggio è di tipo keep-alive, salta al prossimo ciclo
                continue
            
            #direz_decode e' una stringa, con la funzione eval, riesco a convertirla a dizionario
            diz_movimenti = eval(direz_decode)
            print(diz_movimenti)
            lettera = controlloInDizTabella(diz_movimenti)
            print(lettera)

            #.setMotor(left, right)

            #Controllo dei movimenti default (WASD) e richiamo delle funzioni corrispondenti
            if diz_movimenti["w"]:
                #controllo di pressione contemporanea di a oppure d, in tal caso, spostarsi anche a dx/sx
                if diz_movimenti["a"]:
                    alphaBot.setMotor(-50, 25)
                elif diz_movimenti["d"]:
                    alphaBot.setMotor(-25,50)
                else:
                    print("avanti")
                    alphaBot.setMotor(-73, 77)
                    #alphaBot.forward()
            elif diz_movimenti["s"]:
                #controllo di pressione contemporanea di a oppure d, in tal caso, spostarsi anche a dx/sx

                if diz_movimenti["a"]:                
                    alphaBot.setMotor(50,-25)
                elif diz_movimenti["d"]:
                    alphaBot.setMotor(25,-50)
                else:
                    print("indietro")
                    alphaBot.setMotor(73, -77)
            elif diz_movimenti["a"]:
                print("sinistra")
                alphaBot.setMotor(-50, -50)
            elif diz_movimenti["d"]:
                print("destra")
                alphaBot.setMotor(50, 50)
            elif diz_movimenti["n"]:
                alphaBot.setMotor(-86, 94)
            elif lettera != "": #se lettera è nella tabella esegui il comando della tabella
                eseguiComandoTabella(diz_comandi_tabella[lettera])
            else:
                #altrimenti la lettera == "" quindi fermare l'alphabot
                alphaBot.stop()

        except socket.timeout:#se il socket va in timeout gestisce l'alphabot
            if time.time() - last_message_time > TIMEOUT:
                print("Timeout: client non ha inviato dati, considerato disconnesso.")
                alphaBot.stop()
                break

    connection.close()

if __name__ == "__main__":
    main()
