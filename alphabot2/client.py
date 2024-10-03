# PROTOCOLLO DEI MESSAGGI INVIATI AL SERVER
# Usiamo delle stringhe
# 2 tipi di messaggi: richieste (dal client) e risposte (dal server)

# STRUTTURA RICHIESTE (f-string)
# f"{command}|{value}" command possibili: forward, backward, left, right

# STRUTTURA RISPOSTE
# f"{status}|{phrase}" status: ok oppure error, phrase: spiega errore se c'è

# Implementare un client/server tcp che utilizzino questi comandi

import socket
from pynput import keyboard

SERVER_ADDRESS = ("192.168.1.128", 9090)
BUFFER_SIZE = 4096

command = ""

def on_press(key):
    global command

    if key.char == "w":
        print("press w")
    elif key.char == "s":
        print("press s")
    elif key.char == "a":
        print("press a")
    elif key.char == "d":
        print("press d")
    
    command = key.char.lower()

def on_release(key):
    global command

    if key.char == "w":
        print("release w")
    elif key.char == "s":
        print("release s")
    elif key.char == "a":
        print("release a")
    elif key.char == "d":
        print("release d")
    
    command = key.char.upper()

def start_listener():
    with keyboard.Listener(on_press = on_press, on_release = on_release) as listener:
        listener.join()
    
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    start_listener()
    while True:
        s.sendall(command.encode())

    s.close()

if __name__ == "__main__":
    main()