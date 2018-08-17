import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", 65042))
sock.sendall(b"Hello, world")
data = sock.recv(1024)
sock.close()
print(data.decode("utf-8"))
