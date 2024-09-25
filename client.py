import socket

MESSAGE = "Hello, World!"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1",228))
s.sendto(MESSAGE.encode(), ("127.0.0.1", 228))
s.close()