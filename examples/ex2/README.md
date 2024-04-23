# PyChat

Pychat is a chat-box application developed in Python 3.

Pychat consists of two components, a server and a client. 
The program is a TCP server utilizing the socket module, tkinter to serve as a graphical user interface, and threading to allow:
* automatic updating of the chatlog for the client
* multiple clients to join the server.

# Usage

To start a server, open up the directory in a terminal and type:

* python ChatServer.py

Once the server is running, you can can open up a client by typing the following into the terminal:

* python ClientGUI.py

By default, the server starts on port 23456. The client will default to connecting to 127.0.0.1, port 23456, but can be specified in the join menu. 

# Screenshot
![image](https://user-images.githubusercontent.com/78966342/163656163-72ff0e35-1868-448c-8236-5d057d35c647.png)
