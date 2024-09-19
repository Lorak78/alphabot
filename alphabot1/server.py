import socket

MY_ADDRESS = ("192.168.1.122", 9090)
BUFFER_SIZE = 4096

def main():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    
    connection, client_address = s.accept() #bloccante
    print(f"Il client {client_address} si è connesso")

    message = connection.recv(BUFFER_SIZE)
    direz_decode = message.decode()

    direz, dist = direz_decode.split("|")

    print(f"{direz} {dist}")

    status = "ok"
    
    connection.sendall(f"{status}|{direz} {dist}".encode())
    s.close()

if __name__ == "__main__":
    main()