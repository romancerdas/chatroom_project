import socket
from protocol import decode_message

HOST = "127.0.0.1" # Set IP address     # for now, HOST will be set as the localhost IP, will be updated later in development 
PORT = 5000 # Set Port number     # same as IP, set to 5000 for now, will be updated later in development 

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a server side socket using IPv4 address family and TCP protocol 
server.bind((HOST, PORT)) # binds the server socket to the HOST and PORT 
server.listen() # opens socket for connections 

print(f"Server is listening on {HOST}:{PORT}") # Terminal message to states server state (listening)

conn, addr = server.accept() # instantiates conn socket object and address tuple when .accept() runs, which accepts an incoming connection
print(f"Client connected from {addr}") # terminal message that states client connection and client address 

while True:
    data = conn.recv(1024) # assigns data variable to the bytes received from the client, with a 1024 byte buffer 

    if not data: # if no data is received, connection is broken 
        print("Client disconnected.")
        break

    message = decode_message(data) # assigns message variable to the decoded data 

    print("Received message:")
    print(message) # prints message in terminal 

conn.close() # socket connection is closed 
server.close() # server socket is closed 