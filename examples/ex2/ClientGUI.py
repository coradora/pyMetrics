# Cora S.
# PyChat GUI Client
# CSCI 3010 Project

# Imports

import socket as s
from tkinter import *
import threading

# Globals

root=Tk()
name = StringVar()
IP = StringVar()
PORT = StringVar()

# Tkinter Main Window function, draws a window with our chatbox, 
# a text entry box to type messages, a join button, and an exit button

def mainWindow():
    
    # Window name

    root.title("PyChat")
    
    # Widgets

    content = Frame(root)
    a = Label(root, text="Enter message:")
    global T
    T = Text(root, height = 16, width = 48)
    global entry_box
    entry_box = Entry(root)

    # entry box disabled until chatroom is joined
    entry_box.configure(state='disable') 

    join_button = Button(root, text="Join", command=join)
    exit_button = Button(root, text='Exit', command=exit)

    # Allows user to press enter on the window to send message
    # typed into the text entry box.

    root.bind('<Return>', send) 

    # Grid
    content.grid(column=0, row=0)
    T.grid(column=1, row=0, columnspan=3)
    a.grid(column=1, row=1 )
    entry_box.grid(column=2, row=1)
    join_button.grid(column=1, row=2)
    exit_button.grid(column=3, row=2)

    # Tkinter main loop

    root.mainloop()

# Handles joining, name selection

def join():
    newWindow = Toplevel(root)
    content = Frame(newWindow)
    newWindow.title("Join")
    newWindow.geometry("200x100")

    # Labels

    label = Label(newWindow, text= "Enter a username:")
    ip = Label(newWindow, text="IP Address:")
    port = Label(newWindow, text="Port:")

    # Entries

    global nameEntry
    nameEntry = Entry(newWindow, textvariable=name)
    ipEntry = Entry(newWindow, textvariable=IP)
    portEntry = Entry(newWindow, textvariable=PORT)

    # Sets default values for IP/PORT

    ipEntry.insert(0, '127.0.0.1')
    portEntry.insert(0, 23456)

    # Buttons

    joinButton = Button(newWindow, text="Join", command=lambda: nameEntered(newWindow))
    
    # Grid

    content.grid(column=0, row=0)
    label.grid(column=0, row=1)
    nameEntry.grid(column=2, row=1)
    ip.grid(column=0, row=2)
    ipEntry.grid(column=2, row=2)
    port.grid(column=0, row=3)
    portEntry.grid(column=2, row=3)
    joinButton.grid(column=1, row=4)

    # Allows user to press enter on the window to enter data
    # typed into the text entry boxes.

    newWindow.bind('<Return>', lambda eff: name_enter(eff, newWindow)) 

# Function verifies a name 2 characters or greater is entered.
# Destroys the Join window. 
# Initializes the client and connects to the server. 
# Sends the username to the server, and calls the update thread to
# keep the chat box updating.

def nameEntered(newWindow):
    if len(name.get()) >= 2:
        print(f"Username = {name.get()}")
        newWindow.destroy()
        
        global client
        client = s.socket(s.AF_INET, s.SOCK_STREAM)
        client.connect((IP.get(), int(PORT.get()))) 
        client.settimeout(1)
        client.send(name.get().encode())

        # enables the entry box in root window.
        entry_box.configure(state='normal') 

        update()

# Update function is a threaded function that updates the 
# chatbox (T) on the root window every 5 seconds. If no data
# is received, it times out and repeats.

def update():  
    t = threading.Timer(5, update)
    t.daemon = True
    t.start()
    try:     
        received_message = client.recv(2048)
        print(received_message.decode())
        T.insert(END, received_message)
    except s.timeout:
        print('timeout')

# Send function corresponds to the enter key bind in the root window.
# When a message is typed into the entry box and the user presses enter,
# this function checks whether or not a message is actually entered, 
# and sends the message to the server with the name + " >> " appended.
# Example: ("Cora >> Hello world!").

def send(event):
    
    print(f"Sending message: {entry_box.get()}")
    message = entry_box.get()
    if len(message) == 0:
        return
    else:
        message = name.get() + " >> " + message
        client.send(message.encode())
    entry_box.delete(0, END)
    
# Processes the enter key being pressed in the Join window.

def name_enter(event, newWindow):
    nameEntered(newWindow)

# Functions similarly to pressing the X in the window. 
# Closes out of the application when exit is pressed in the root window.

def exit():
    root.destroy()

if __name__ == '__main__':
    mainWindow()