# Overview

This project is a multi-room chatroom application built using Python socket programming and Tkinter. The application allows multiple users to connect to a central server, join chat rooms, and communicate with each other in real time through either a command-line client or a graphical user interface (GUI) client.

The project was developed to strengthen my understanding of network communication, multithreading, client-server architecture, and GUI development. One of my main goals was to learn how backend networking systems interact with a frontend graphical interface while maintaining responsive real-time communication between multiple users. The server handles multiple clients simultaneously using Python threads and routes messages only to users within the same room.

To start the server: Run `python server.py` in your terminal

To start the client: Run `python client_cli.py` or `python client_gui.py`, depending on if you want to run it in your terminal, or with the GUI.

[Chatroom App Video Demo](https://youtu.be/whXkLv8Y0zU)

# Network Communication

This project uses a client-server architecture. A central server accepts incoming TCP connections from multiple clients and manages message routing between chat rooms. Clients communicate only through the server rather than directly with each other. This version runs on localhost (IP:127.0.0.1:5000). Messages between the client and server are formatted as JSON objects and encoded into UTF-8 bytes before being transmitted over the network. The server decodes incoming JSON messages, determines the message type, and processes the request accordingly.

# Development Environment

- Python 3
- Visual Studio Code 
- Windows 11 
- Git / Github 

Python Libraries 
- socket 
- threading
- tkinter 
- json

# Useful Websites

* [Official "socket" library Documentation](https://docs.python.org/3.14/library/socket.html#socket.socket.connect)
* [How to use "socket" library](https://docs.python.org/3/howto/sockets.html)
* [Official "tkinter" Documentation](https://docs.python.org/3/library/tkinter.html)
* [Official "threading" Documentation](https://docs.python.org/3/library/threading.html)

# Future Work

* Improve GUI design and layout
* Improve room management and allow users to create rooms from the GUI
* Add support for hosting across multiple machines instead of localhost only
