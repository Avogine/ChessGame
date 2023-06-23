import socket
import sys
import Terminal_GUI

host = "0.0.0.0"
port = 1337
buffer = 1024
accept = "2342"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def Online_Game():
# Start Connection
    i = input("[T] Wait or Connect: ")
    if not i:
        r.bind((host, port))
        r.listen(5)
        print("[T] Waiting for connection")
        client_socket, address = r.accept()
        address, dk = address
        print(f"[T] {address} just connected")
        mode = client_socket.recv(buffer).decode("utf-8")
        print(f"[T] {address} wants to play a {mode} Game.")
        a = input(f"[T] Accept (Y/N): ")
        name = input("[T] Name of your opponent: ")
        if not name:
            name = str(address)
        if a == "Y":
            s.connect((address, port))
            s.send(f"{accept}".encode("utf-8"))
        else:
            s.connect((address, port))
            s.send(f"13".encode("utf-8"))
            s.close()
            r.close()
            Online_Game()
    else:
        m = input("[T] What mode do you want to play: ")
        if not m:
            m = "normal"
        r.bind((host, port))
        r.listen(5)
        s.connect((i, port))
        s.send(f"{m}".encode("utf-8"))
        client_socket, address = r.accept()
        ans = client_socket.recv(buffer).decode("utf-8")
        print(ans)
        if ans != accept:
            s.close()
            r.close()
            Online_Game()




    while True:  # start
        Terminal_GUI.term_render()

        pos = input(f"[{turn()}] Select: ")
        if pos == "render":
            pass
        else:
            select(pos)





Online_Game()