import socket

HOST = "localhost"
PORT = 8080

info = socket.getaddrinfo(HOST, PORT, proto=socket.IPPROTO_TCP)
sock_addr = info[0][4]  # ('::1', 8080, 0, 0)

with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as s:
    s.connect(sock_addr)
    print("It's a client!")

    while True:
        ack = input("My message will be: ")
        if ack == "close":
            print("Goodbye cruel world")
            break
        s.sendall(f"{ack}".encode())
        data = s.recv(1024).decode("utf-8")
        print(f"Answer from server: {data}")
