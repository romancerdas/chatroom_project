import socket
import threading
from protocol import decode_message

HOST = "127.0.0.1" # Set IP address     # for now, HOST will be set as the localhost IP, will be updated later in development 
PORT = 5000 # Set Port number     # same as IP, set to 5000 for now, will be updated later in development 

clients = [] # an array to hold multiple clients

def handle_client(conn, addr):
    print(f"New Client has connected [{addr}]") # terminal message to states client connection and client address
    clients.append(conn) # appends socket object to client array
    while True:
        try:
            data = conn.recv(1024) # assigns incoming 1024 bytes to data variable 

            if not data: # break connection if no data is received 
                break

            message = decode_message(data) # assigns message variable to the decoded data
            print(f"Incoming message from {addr}: {message}") # print message and sender address in recipient terminal 

            for client in clients: # send message to all clients in client array 
                if client != conn: # if the client is not the sender, send the message to the client 
                    client.send(data) # sends the data to the client

        except: # error handling (i.e. disconnection)
            break

    print(f"Client has disconnected [{addr}]") # terminal message to states client disconnection and client address
    if conn in clients: 
        clients.remove(conn) # removes client socket object from client array
    conn.close() # closes the client socket connection

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a server side socket using IPv4 address family and TCP protocol 
server.bind((HOST, PORT)) # binds the server socket to the HOST and PORT 
server.listen() # opens socket for connections 

print(f"Server is listening on {HOST}:{PORT}") # Terminal message to states server state (listening)

while True: 
    conn, addr = server.accept() # instantiates conn socket object and address tuple when .accept() runs, which accepts an incoming connection
    thread = threading.Thread(target=handle_client, args=(conn,addr)) # creates a new thread to run handle_client(), and passes conn and addr arguements 
    thread.start() # starts the thread

    print(f"Active Connections: {threading.active_count() - 1}") # shows number of active connections, -1 to account for main thread 
    