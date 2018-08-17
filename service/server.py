import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 65042))
sock.listen(True)

while True:
    conn, addr = sock.accept()
    print('Connected by', addr)
    data = conn.recv(1024)
    conn.sendall(data)