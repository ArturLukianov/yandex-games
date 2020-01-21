import socket
import threading

def new_client(conn, addr):
    data = conn.recv(1024)
    print(f"[Connected {addr[0]}]")
    print("[" + str(addr) + " : " + data.decode("UTF-8") + "]")
    if data.decode("UTF-8") != "CT":
        print("Error durning connection")
        conn.close()
        return
    conn.send(b"CA")
    print("[Connection OK]")
    conn_alive = 1
    while conn_alive:
        data = conn.recv(1024)
        if not data:
            conn_alive = 0
        print("[" + str(addr) + " : " + data.decode("UTF-8") + "]")
        conn.send(b"RA")
    conn.close()

tp = input("s/c : ")

if tp == "s":
    sock = socket.socket()
    sock.bind(('', 9090))
    sock.listen(10)
    while True:
        conn,addr = sock.accept()
        threading.Thread(target=new_client, args=(conn,addr)).start()
elif tp == "c":
    sock = socket.socket()
    ip = input()
    sock.connect((ip, 9090))
    conn_alive = True
    sock.send(b"CT")
    data = sock.recv(1024).decode("UTF-8")
    if data == "CA":
        while conn_alive:
            sock.send(b"INFO")
            data = sock.recv(1024)
            if not data:
                conn_alive = 0
            print("[Server : " + data.decode("UTF-8") + "]")
    sock.close()
else:
    print("Wrong network settings")
