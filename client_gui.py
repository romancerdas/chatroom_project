import socket
import threading
import tkinter as tk
from protocol import encode_message, decode_message

HOST = "127.0.0.1"
PORT = 5000

client = None
username = ""
room = ""
running = False


def add_chat_message(text):
    chat_display.config(state=tk.NORMAL)
    chat_display.insert(tk.END, text + "\n")
    chat_display.config(state=tk.DISABLED)
    chat_display.see(tk.END)


def receive_messages():
    global running

    while running:
        try:
            data = client.recv(1024)

            if not data:
                root.after(0, add_chat_message, "Disconnected from server.")
                running = False
                break

            message = decode_message(data)

            if message["type"] == "SEND_MESSAGE":
                display_text = f"[{message.get('room', '')}] {message['username']}: {message['message']}"
                root.after(0, add_chat_message, display_text)

        except Exception as e:
            root.after(0, add_chat_message, f"Connection error: {e}")
            running = False
            break


def connect_to_server():
    global client, username, room, running

    username = username_entry.get().strip()
    room = room_entry.get().strip()

    if username == "" or room == "":
        add_chat_message("Username and room are required.")
        return

    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        join_message = {
            "type": "JOIN_ROOM",
            "username": username,
            "room": room
        }

        client.send(encode_message(join_message))

        running = True

        receive_thread = threading.Thread(target=receive_messages, daemon=True)
        receive_thread.start()

        add_chat_message(f"Connected as {username} in room [{room}]")

        connect_button.config(state=tk.DISABLED)

    except Exception as e:
        add_chat_message(f"Could not connect: {e}")


def send_message():
    text = message_entry.get().strip()

    if text == "":
        return

    if not running:
        add_chat_message("Not connected to server.")
        return

    message = {
        "type": "SEND_MESSAGE",
        "username": username,
        "room": room,
        "message": text
    }

    try:
        client.send(encode_message(message))
        add_chat_message(f"[{room}] {username}: {text}")
        message_entry.delete(0, tk.END)

    except Exception as e:
        add_chat_message(f"Send failed: {e}")


def close_app():
    global running

    running = False

    if client:
        client.close()

    root.destroy()


root = tk.Tk()
root.title("Chatroom Client")
root.geometry("500x500")

top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Username:").grid(row=0, column=0)
username_entry = tk.Entry(top_frame)
username_entry.grid(row=0, column=1)

tk.Label(top_frame, text="Room:").grid(row=1, column=0)
room_entry = tk.Entry(top_frame)
room_entry.grid(row=1, column=1)

connect_button = tk.Button(top_frame, text="Connect", command=connect_to_server)
connect_button.grid(row=2, column=0, columnspan=2, pady=5)

chat_display = tk.Text(root, state=tk.DISABLED, height=20, width=60)
chat_display.pack(padx=10, pady=10)

bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

message_entry = tk.Entry(bottom_frame, width=40)
message_entry.grid(row=0, column=0, padx=5)

send_button = tk.Button(bottom_frame, text="Send", command=send_message)
send_button.grid(row=0, column=1)

root.protocol("WM_DELETE_WINDOW", close_app)

root.mainloop()