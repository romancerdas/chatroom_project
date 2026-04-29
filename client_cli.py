import socket
from protocol import encode_message

HOST = "127.0.0.1"
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter username: ")

while True:
    text = input("Enter message, or type quit: ")

    if text.lower() == "quit":
        break

    message = {
        "type": "SEND_MESSAGE",
        "username": username,
        "message": text
    }

    client.send(encode_message(message))

client.close()