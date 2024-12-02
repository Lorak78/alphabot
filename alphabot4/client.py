import socket
from pynput import keyboard
import time
import threading

SERVER_ADDRESS = ("192.168.1.129", 9090)
BUFFER_SIZE = 4096
KEEP_ALIVE_INTERVAL = 5 #il messaggio keep-alive si manda ogni 5 secondi

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creazione socket tcp
s.connect(SERVER_ADDRESS) #connessione al server
diz_mess = {"w": False, "a": False, "s": False, "d": False, "n": False} #dizionario delle direzioni basilari, tutte a false

def on_press(key): #funzione chiamata in un thread ogni volta che si preme un tasto
    global diz_mess
    
    print(key.char)
    
    if key.char in diz_mess.keys(): #se il tasto premuto si trova tra le chiavi del dizionario
        if diz_mess[key.char] != True: #ed e' false
            diz_mess[key.char] = True #attiva quindi il tasto nel dizionario
            s.sendall(f"{diz_mess}".encode()) #manda il messaggio solo quando cambia in true un valore del dizionario
    else:
        diz_mess[key.char] = True #se non è nel dizionario lo attivo
        s.sendall(f"{diz_mess}".encode()) #lo mando perche' il server lo gestirà

def on_release(key): #funzione chiamata in un thread ogni volta che si rilascia un tasto premuto
    global diz_mess
    
    print(key.char)
    
    if key.char in diz_mess.keys():
        diz_mess[key.char] = False #disattivo il tasto nel dizionario
    
    s.sendall(f"{diz_mess}".encode())

def start_listener(): #Thread delle funzioni che controllano la premuta dei tasti
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def send_keep_alive(): #altro thread che serve a mandare il keep-alive ogni interval secondi
    while True:
        s.sendall("KEEP-ALIVE".encode())
        time.sleep(KEEP_ALIVE_INTERVAL)

def main():
    keep_alive_thread = threading.Thread(target=send_keep_alive)
    keep_alive_thread.daemon = True
    keep_alive_thread.start() #start del thread del keep-alive

    start_listener() # start dei thread della premuta dfei tasti

    s.close()

if __name__ == "__main__":
    main()
