import socket
from pynput import keyboard
import time
import threading

SERVER_ADDRESS = ("10.210.0.93", 9090)
BUFFER_SIZE = 4096
KEEP_ALIVE_INTERVAL = 5  # Invia un keep-alive ogni 5 secondi

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(SERVER_ADDRESS)
diz_mess = {"w": False, "a": False, "s": False, "d": False}

def on_press(key):
    global diz_mess

    if key.char == "w":
        print("press w")
    elif key.char == "s":
        print("press s")
    elif key.char == "a":
        print("press a")
    elif key.char == "d":
        print("press d")
    
    if key.char in "wasd":
        if diz_mess[key.char] != True:
            diz_mess[key.char] = True
            s.sendall(f"{diz_mess}".encode())

def on_release(key):
    global diz_mess

    if key.char == "w":
        print("release w")
    elif key.char == "s":
        print("release s")
    elif key.char == "a":
        print("release a")
    elif key.char == "d":
        print("release d")
    
    if key.char in "wasd":
        diz_mess[key.char] = False
    
    s.sendall(f"{diz_mess}".encode())

def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Funzione per inviare periodicamente i messaggi di keep-alive
def send_keep_alive():
    while True:
        s.sendall("KEEP-ALIVE".encode())  # Invia il messaggio di keep-alive
        time.sleep(KEEP_ALIVE_INTERVAL)  # Attendi l'intervallo specificato

def main():
    # Avvia il thread per il keep-alive
    keep_alive_thread = threading.Thread(target=send_keep_alive)
    keep_alive_thread.daemon = True  # Si chiuderà automaticamente quando il main thread termina
    keep_alive_thread.start()

    # Avvia l'ascoltatore di tastiera per inviare comandi
    start_listener()

    s.close()

if __name__ == "__main__":
    main()
