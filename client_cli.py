import socket
from protocol import encode_message

HOST = "127.0.0.1" # Set IP address     # for now, HOST will be set as the localhost IP, will be updated later in development 
PORT = 5000 # Set Port number     # same as IP, set to 5000 for now, will be updated later in development 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # creates a server side socket using IPv4 address family and TCP protocol 
client.connect((HOST, PORT)) # connects to the client socket at HOST and PORT 

username = input("Enter username: ") # user inputs a username 

while True: # message compiler loop
    text = input("Enter message, or type quit: ") # user types a message or quits 

    if text.lower() == "quit": # checks if user wants to quit 
        break

    message = { # JSON composition of the message to be sent to server 
        "type": "SEND_MESSAGE",
        "username": username,
        "message": text
    }

    client.send(encode_message(message)) # client sockets sends the encoded message to the server 

client.close() # client socket closes 