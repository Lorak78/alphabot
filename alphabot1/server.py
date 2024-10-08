import socket, AlphaBot

MY_ADDRESS = ("192.168.1.128", 9090)
BUFFER_SIZE = 4096

def main():
    alphaBot = AlphaBot.AlphaBot()
    alphaBot.stop()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    
    connection, client_address = s.accept() #bloccante
    print(f"Il client {client_address} si è connesso")

    while True:
        message = connection.recv(BUFFER_SIZE)
        direz_decode = message.decode()

        direz, dist = direz_decode.split("|")

        print(f"{direz} {dist}")

        if direz == "forward":
            alphaBot.forward()
        elif direz == "backward":
            alphaBot.backward()
        elif direz == "left":
            alphaBot.left()
        elif direz == "right":
            alphaBot.right()
        elif direz == "stop":
            alphaBot.stop()
        
        connection.sendall(direz.encode())
    
    s.close()

if __name__ == "__main__":
    main()