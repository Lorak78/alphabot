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

        print(f"{direz_decode}")

        if direz_decode == "w":
            alphaBot.forward()
        elif direz_decode == "s":
            alphaBot.backward()
        elif direz_decode == "a":
            alphaBot.left()
        elif direz_decode == "d":
            alphaBot.right()
        elif direz_decode.isupper():
            alphaBot.stop()
    
    s.close()

if __name__ == "__main__":
    main()