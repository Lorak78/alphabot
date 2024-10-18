import socket , AlphaBot

MY_ADDRESS = ("127.0.0.1", 9090)
BUFFER_SIZE = 4096

alphaBot = AlphaBot.AlphaBot()

def main():
    global conta_ping
    alphaBot.stop()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(MY_ADDRESS)
    s.listen()
    
    connection, client_address = s.accept() #bloccante
    print(f"Il client {client_address} si è connesso")

    while True:
        message = connection.recv(BUFFER_SIZE)
        direz_decode = message.decode()

        diz_movimenti = eval(direz_decode) #trasforma l'fstring in dizionario

        #.setMotor(left, right)
        if diz_movimenti["w"] == True:
            if diz_movimenti["a"] == True:
                print("avanti sinistra")
                alphaBot.setMotor(25, -50)
            elif diz_movimenti["d"] == True:
                print("avanti destra")
                alphaBot.setMotor(-50, 25)
            else:
                print("avanti")
                alphaBot.forward()
        elif diz_movimenti["s"] == True:
            if diz_movimenti["a"] == True:
                print("indietro sinistra")
                alphaBot.setMotor(-25, 50)
            elif diz_movimenti["d"] == True:
                print("indietro destra")
                alphaBot.setMotor(50, -25)
            else:
                print("indietro")
                alphaBot.backward()
        elif diz_movimenti["a"] == True:
            print("sinistra")
            alphaBot.left()
        elif diz_movimenti["d"] == True:
            print("destra")
            alphaBot.right()
        elif all(not valore for valore in diz_movimenti.values()):
            print("stop")
            alphaBot.stop()
    
    s.close()

if __name__ == "__main__":
    main()