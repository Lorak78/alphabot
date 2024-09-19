# PROTOCOLLO DEI MESSAGGI INVIATI AL SERVER
# Usiamo delle stringhe
# 2 tipi di messaggi: richieste (dal client) e risposte (dal server)

# STRUTTURA RICHIESTE (f-string)
# f"{command}|{value}" command possibili: forward, backward, left, right

# STRUTTURA RISPOSTE
# f"{status}|{phrase}" status: ok oppure error, phrase: spiega errore se c'è

# Implementare un client/server tcp che utilizzino questi comandi

import socket

SERVER_ADDRESS = ("192.168.1.122", 9090)
BUFFER_SIZE = 4096

d = {1:"forward",
     2:"backward",
     3:"left",
     4:"right"}

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(SERVER_ADDRESS)
    command = 0
    while command < 1 or command > 4: 
        command = int(input("inserisci un comando:\n\
1:forward\n2:backward\n3:left\n4:right\n"))
    
    value = int(input("inserisci la distanza: "))
    s.sendall(f"{d[command]}|{value}".encode())

    message = s.recv(BUFFER_SIZE)

    print(f"{message.decode()}")

    s.close()

if __name__ == "__main__":
    main()