import socket
import sys

s = socket.socket()
r = socket.socket()
def connect(host, ip, port = 1337):
    s.connect((host, port))
    s.send(f"{ip}".encode())
def send(data,buffer=1024):
    if not sys.getsizeof(data) > buffer:
        s.send(f"{data}".encode())
def end_con():
    s.close()
def listen(host="0.0.0.0",port=1337):
    r.bind((host, port))
    r.listen(5)
def receive( buffer=1024):

    client_socket, address = r.accept()
    data = client_socket.recv(buffer).decode()

    client_socket.close()
    r.close()
    return(data)
def end_listen():
    r.close()


