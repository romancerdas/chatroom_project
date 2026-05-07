import socket
import threading
from protocol import decode_message

HOST = "127.0.0.1" # Set IP address     # for now, HOST will be set as the localhost IP, will be updated later in development 
PORT = 5000 # Set Port number     # same as IP, set to 5000 for now, will be updated later in development 

clients = [] # an array to hold multiple clients
rooms = {
    "general": []
}

client_rooms = {}

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

            if message["type"] == "JOIN_ROOM": # checks if the message is a request to join a room
                room = message["room"]
                if room not in rooms:
                    rooms[room] = []
                if conn not in rooms[room]:
                    rooms[room].append(conn)
                client_rooms[conn] = room 

                print(f"{addr} has joined room {room}")

            if message["type"] == "SEND_MESSAGE":
                room = client_rooms.get(conn)

                if room:
                    for client in rooms[room]:
                        if client != conn:
                            try:
                                client.send(data)
                            except Exception as e:
                                print(f"Failed to send message: {e}")       

            if message["type"] == "LEAVE_ROOM":
                room = message["room"]

                if room in rooms and conn in rooms[room]:
                    rooms[room].remove(conn)

                if conn in client_rooms: 
                    del client_rooms[conn]

                print(f"{message['username']} has left the room {room}.")

                continue


        except Exception as e:
            print(f"Server error with {addr}: {e}")
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
    