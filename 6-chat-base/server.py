"""
 Implements a simple socket server

"""

import socket
import threading
from datetime import datetime


# class for a chat room
class ChatRoom:

    def __init__(self, name, moderator):
        self.name = name
        self.userList = []
        self.moderator = moderator


# Class for the client
class Client:
    def __init__(self, name, connection):
        self.name = name
        self.connection = connection


def handle_client(name, client_connection):
    while True:

        # Print message from client
        msg = client_connection.recv(1024).decode()
        now = datetime.now()
        print(now.strftime("%H:%M:%S"))
        print('Received: ({}) - {}'.format(name, msg))

        msg = interpreter(msg)

        if msg == "function action":
            continue

        # Check for exit
        if msg == 'exit':
            goodbyeMsg = "Goodbye {}".format(name)
            client_connection.sendall(goodbyeMsg.encode())
            break

        # Return message to client
        for user in connectionList:
            if user != client_connection:
                msgSend = "({}) {}".format(name, msg)
                user.sendall(msgSend.encode())

    # Close client connection
    print('Client disconnected...')
    connectionList.remove(client_connection)
    for user in connectionList:
        msgSend = "User {} has disconected".format(name)
        user.sendall(msgSend.encode())

    client_connection.close()


# Create a new room
def create_room(roomName, moderatorName):
    newRoom = ChatRoom(roomName, moderatorName)
    connectionList.append(newRoom)


# Join's a new room
def join_room(roomName, client):

    # find if the room exist
    for room in connectionList:
        if room.name == roomName:
            room.userList.append(client)


def interpreter(msg, user):
    msgArray = msg.split()

    # If it doesn't have the function indicator("/") it returns the message to send to the chat
    if msgArray[0][0] != "/":
        return msg

    #   (/create roomName)
    if msgArray[0] == "/create":
        print("Create")
        create_room(msgArray[1], user)
    if msgArray[0] == "/join":
        print("join - not implement")
    if msgArray[0] == "/kick":
        print("kick - not implement")
    if msgArray[0] == "/ban":
        print("ban - not implement")
    if msgArray[0] == "/whisper":
        print("whisper - not implement")


    return "function action"


# roomList = [create_room("#Geral", )]
connectionList = []

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # waiting for the username
    username = client_connection.recv(1024).decode()
    msg = "You are now connected, {}!".format(username)
    client_connection.sendall(msg.encode())
    # Send for all the user in the room
    for user in connectionList:
        msgSend = "User {} has appeared".format(username)
        user.sendall(msgSend.encode())

    connectionList.append(client_connection)
    # Cria thread
    thread = threading.Thread(target=handle_client, args=(username, client_connection))

    thread.start()

# Close socket
server_socket.close()
