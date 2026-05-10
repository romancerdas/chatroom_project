import socket
import threading
from protocol import encode_message, decode_message 

HOST = "127.0.0.1" # Set IP address     # for now, HOST will be set as the localhost IP, will be updated later in development 
PORT = 5000 # Set Port number     # same as IP, set to 5000 for now, will be updated later in development 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a server side socket using IPv4 address family and TCP protocol 
client.connect((HOST, PORT)) # connects to the client socket at HOST and PORT 

username = input("Enter username: ") # user inputs a username 
room = input("Enter room name: ")

running = True # variable to control loops

join_message = {
    "type": "JOIN_ROOM",
    "username": username,
    "room": room
}

client.send(encode_message(join_message)) 


def receive_messages(): # defines how to handle incoming messages 

    global running # allows function to modify the variable "running"

    while running:
        try:
            data = client.recv(1024) # assigns incoming 1024 bytes to data variable 

            if not data: # break connection if no data is received 
                print("Disconnected from server.") # terminal message to state disconnection from server
                running = False # sets "running" to false to break loop
                break 

            message = decode_message(data) # assigns message variable to the decoded data

            if message["type"] == "SEND_MESSAGE":
                print(f"\n [{message['username']}]: {message['message']}") # prints incoming message to terminal 
                print("Enter message, or type 'quit': ", end="") # reprints message prompt after incoming message is printed

        except: # error handling (i.e. disconnection)
            break 



thread = threading.Thread(target=receive_messages) # creates a new thread to run receive_messages()
thread.daemon = True # sets thread as a daemon thread, meaning the process will end when the main thread ends 
thread.start() # starts the thread 


while True: # message compiler loop
    text = input("Enter message, or type quit: ") # user types a message or quits 

    if text.lower() == "leave": 
            leave_message = {
                "type": "LEAVE_ROOM",
                "username": username,
                "room": room
            }   
            client.send(encode_message(leave_message))
            (print(f"You have left the room {room}."))

            room = input("Enter room name: ")

            join_message = {
                "type": "JOIN_ROOM",
                "username": username,
                "room": room
            }

            client.send(encode_message(join_message))

            continue 
    
    
    if text.lower() == "quit": # checks if user wants to quit 
        break

    

    message = { # JSON composition of the message to be sent to server 
        "type": "SEND_MESSAGE",
        "username": username,
        "room": room,
        "message": text
    }

    client.send(encode_message(message)) # client sockets sends the encoded message to the server 

client.close() # client socket closes 