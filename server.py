import socket
from protocol import decode_message

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Server is listening on {HOST}:{PORT}")

conn, addr = server.accept()
print(f"Client connected from {addr}")

while True:
    data = conn.recv(1024)

    if not data:
        print("Client disconnected.")
        break

    message = decode_message(data)

    print("Received message:")
    print(message)

conn.close()
server.close()