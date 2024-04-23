# Cora S.
# PyChat Server
# CSCI 3010 Project

# Imports

import socket as s
import time
import threading

# Constants

IP = '127.0.0.1' # localhost
PORT = 23456
client_list = []

# Threaded function.
# Each instance of client communicating with the server socket
# is sending data to the server as well as broadcasting to each
# client connected to the server.

def new_client(conn, addr):
    conn.send(b'Welcome to pyChat!\n')
    while True:
        data = conn.recv(2048)
        if not data:
            time.sleep(5)
        newStr = data.decode()
        if '>>' not in newStr:
            message = f"{newStr} has joined the chat.\n"
        else:
            message = newStr + "\n"
        broadcast(message, conn)

# Broadcast
# Iterates through clients in client list and sends message to each.

def broadcast(message, conn):
    for client in client_list:
        client.send(message.encode())

# Server socket initialization

def server():
    # SOCK_STREAM due to being TCP connection.
    server = s.socket(s.AF_INET, s.SOCK_STREAM)
    server.bind((IP, PORT))
    # Listens for up to 5 concurrent connections.
    server.listen(5)
    print("Server ready. Accepting incoming connections.")
    # Each client that connects gets threaded to the new_client function.
    while True:
        client, addr = server.accept()
        client_list.append(client)
        threading.Thread(target=(lambda:new_client(client,addr))).start()

if __name__ == '__main__':
    server()