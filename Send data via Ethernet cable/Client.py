import socket


TCP_IP = '127.0.0.1'
TCP_PORT = 62
BUFFER_SIZE = 20
MESSAGE = "Hello Tiw"

while 1:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(bytes(str(MESSAGE),encoding='UTF-8'))
    data = s.recv(BUFFER_SIZE)
    s.close()

    print("received data:", data)
