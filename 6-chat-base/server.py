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

    def __str__(self):
        str = "Room : {} \n Moderator : {}".format(self.name, self.moderator)
        return str


# Class for the client
class Client:
    def __init__(self, name, connection):
        self.name = name
        self.connection = connection
        # in the beginning, the user start's in #Geral
        self.currentRoom = "#Geral"

    def __str__(self):
        str = "Username : {}, Current Room : {}".format(self.name, self.currentRoom)
        return str


def handle_client(client):
    while True:

        # Print message from client
        msg = client.connection.recv(1024).decode()
        now = datetime.now()
        print(now.strftime("%H:%M:%S"))
        print('Received: ({}) - {}'.format(client.name, msg))

        msg = interpreter(msg, client)
        room = find_chatroom(client.currentRoom)

        if msg == "function action":
            continue

        # Check for exit
        if msg == 'exit function':
            goodbyeMsg = "Goodbye {}".format(client.name)
            client.connection.sendall(goodbyeMsg.encode())
            break

        # Return message to client
        for user in room.userList:
            if user != client:
                msgSend = "({}) {}".format(client.name, msg)
                user.connection.sendall(msgSend.encode())

    # Close client connection
    print('Client disconnected...')

    room.userList.remove(client)
    # Send to the rest of the user's of the room
    for user in room.userList:
        msgSend = "User {} has disconected".format(client.name)
        user.connection.sendall(msgSend.encode())

    client.connection.close()


def find_chatroom(room_name):
    for room in roomList:
        if room.name == room_name:
            return room
    return None


# Join's a new room
def join_room(roomName, client):

    # find if the room exist
    for room in roomList:
        if room.name == roomName:
            room.userList.append(client)
            client.currentRoom = room


def create_room(room_name, host_name):
    roomList.append(ChatRoom("#" + room_name, host_name))


# interpreter function
def interpreter(msg, user):
    msgArray = msg.split()

    # If it doesn't have the function indicator("/") it returns the message to send to the chat
    if msgArray[0][0] != "/":
        return msg

    elif msgArray[0] == "/help":
        helpmsg = "Commands avaliable: \n" \
                  "/create (room name); \n" \
                  "/join (room name);\n"
        user.connection.sendall(helpmsg.encode())
    #   (/create roomName)
    elif msgArray[0] == "/create":
        print("Created the room {}".format(msgArray[1]))
        # user.connection.sendall("Not implemented")
        create_room(msgArray[1], user)

    elif msgArray[0] == "/join":
        # user.connection.sendall("Not implemented")
        # user.connection.sendall("Not implemented")
        join_room(msgArray[1], user)

    elif msgArray[0] == "/kick":
        print("kick - not implement")
        user.connection.sendall("Not implemented")

    elif msgArray[0] == "/ban":
        print("ban - not implement")
        user.connection.sendall("Not implemented")

    elif msgArray[0] == "/whisper":
        print("whisper - not implement")
        user.connection.sendall("Not implemented")

    elif msgArray[0] == "/list":
        str = "List of Rooms:\n"
        for room in roomList:
            str += room.__str__() + "\n"
        user.connection.sendall(str.encode())

    elif msgArray[0] == "/userlist":
        for room in roomList:
            for user in room.userList:
                print(user)

    elif msgArray[0] == "/exit":
        return "exit function"

    return "function action"


# create the first room
roomList = [ChatRoom("#Geral", "No One")]
connectionList = []         # connection of user's

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

    # Waiting for the username
    username = client_connection.recv(1024).decode()

    client = Client(username, client_connection)

    msg = "You are now connected, {}!".format(username)
    client_connection.sendall(msg.encode())
    client_connection.sendall("You are in #Geral".encode())
    # Send for all the user in the room

    for user in roomList[0].userList:
        msgSend = "User {} has appeared".format(username)
        user.connection.sendall(msgSend.encode())
    connectionList.append(client)


    roomList[0].userList.append(client)
    # Create a thread to accommodate the client
    thread = threading.Thread(target=handle_client, args=(client, ))

    thread.start()

# Close socket
server_socket.close()
