import socket

HOST = "localhost"
PORT = 8080

# socket.getaddrinfo() get host and port and return information 
# about connect with right socket address (special for IPv6)
info = socket.getaddrinfo(HOST, PORT, proto=socket.IPPROTO_TCP)
sock_addr = info[0][4]  # ('::1', 8080, 0, 0)

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
    s.bind(sock_addr)
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"It's a server!\nConnected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                print("OK bye")
                break
            msg = data.decode("utf-8")
            print(f"Get message: {msg}")
            conn.sendall(data.upper())
