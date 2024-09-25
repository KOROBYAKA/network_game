import socket

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", 228))
    s.listen(1)


    conn, addr = s.accept()
    print(addr)
    while True:
        data = conn.recv(1024)
        print(data)
        conn.close()