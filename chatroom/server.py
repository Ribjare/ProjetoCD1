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
        self.moderator = [moderator]
        self.banList = []
        self.password = None

    def __str__(self):
        str = "Room : {} \n Moderator : {}".format(self.name, self.moderator)

        str += "\n Password : "

        if self.password is not None:
            str += "Protected"
        else:
            str += "None"

        str += "\n Limit of users : "

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
        # client.connection.sendall("Write /help to see all the commands".encode())
        # Print message from client
        msg = client.connection.recv(1024).decode()
        now = datetime.now()
        print(now.strftime("%H:%M:%S"))
        print('Received: ({}) - {}'.format(client.name, msg))

        try:
            msg = interpreter(msg, client)
        except ValueError as error:
            print(error)
            client.connection.sendall(error.__str__().encode())

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


def find_user_in_room(username, room):
    for use in room.userList:
        if use.name == username:
            return use
    return None


def is_user_banned(name, room):
    for clients in room.banList:
        if clients == name:
            return True
    return False


def find_user(username):
    for room in roomList:
        for use in room.userList:
            if use.name == username:
                return use
    return None


# Join's a new room
def join_room(roomName, client):

    # find if the room exist
    room = find_chatroom(roomName)

    if room is None:
        client.connection.sendall("Room not existent".encode())
        raise ValueError("Room not existent")

    if is_user_banned(client.name, room):
        raise ValueError("User is banned from this room")

    if room.password is not None:
        client.connection.sendall("Password?".encode())
        password = client.connection.recv(1024).decode()
        if password != room.password:
            raise ValueError("Incorrect Password")

    room.userList.append(client)
    exRoom = find_chatroom(client.currentRoom)
    exRoom.userList.remove(client)
    client.currentRoom = room.name

    # Send a msg to the user
    str = "You are now in {}".format(roomName)
    client.connection.sendall(str.encode())

    # alert the other users of the room
    msgSend = "User {} has appeared".format(client.name)
    for use in room.userList:
        use.connection.sendall(msgSend.encode())


def is_mod_in_room(use, room):
    for mods in room.moderator:
        print(mods + " == " + use.name)
        if mods == use.name:
            return True
    return False


# interpreter function
def interpreter(msg, client):
    msgArray = msg.split()

    # If it doesn't have the function indicator("/") it returns the message to send to the chat
    if msgArray[0][0] != "/":
        return msg

    # send the collection of commands available
    elif msgArray[0] == "/help":
        helpmsg = "Commands available: \n" \
                  "/create (room name) (password - optional ) - Creates a new room; \n" \
                  "/join #(room name) - Join a existing room;\n" \
                  "/userlist - Show's the online users; \n" \
                  "/list - Show's all the existing rooms;\n" \
                  "/whisper (username) (msg) - Send a private message to a user; \n" \
                  "/kick (username) - Kick's a user from a chat room (Moderator);\n" \
                  "/ban (username) - Permentaly ban's a user from a chat room (Moderator); \n" \
                  "/givemod (username) - Gives moderator status in your room (Moderator)\n" \
                  "/broadcast (msg) - Send to all users in the server a message(Super Moderator)\n"
        client.connection.sendall(helpmsg.encode())

    #   creates a new room
    elif msgArray[0] == "/create":
        room_name = msgArray[1]

        room = find_chatroom("#" + room_name)
        if room is not None:
            raise ValueError("Name already in use")

        room = ChatRoom("#" + room_name, client.name)

        if len(msgArray) == 3:
            room.password = msgArray[2]

        roomList.append(room)
        client.connection.sendall(("The room #" + room_name + " was created").encode())

    # join's a room
    elif msgArray[0] == "/join":
        try:
            join_room(msgArray[1], client)
        except ValueError as error:
            print(error)
            client.connection.sendall(error.__str__().encode())
        except IndexError:
            client.connection.sendall("It need's a second argument".encode())

    # kick a user - moderator command
    elif msgArray[0] == "/kick":
        room = find_chatroom(client.currentRoom)
        try:
            userKick = find_user_in_room(msgArray[1], room)

            if is_mod_in_room(client, room):
                room.userList.remove(userKick)
                userKick.connection.sendall(("You got kicked from " + room.name).encode())

                join_room("#Geral", userKick)

                warningMSG = "User {} was kicked from this room".format(userKick.name)
                for users in room.userList:
                    users.connection.sendall(warningMSG.encode())
            else:
                client.connection.sendall("You don't have permission in this room".encode())
        except IndexError as error:
            client.connection.sendall("It need's a second argument".encode())

    # ban a user for a time or permanent - moderator command
    elif msgArray[0] == "/ban":

        room = find_chatroom(client.currentRoom)
        if not is_mod_in_room(client, room):
            raise ValueError("It's not mod")

        userBan = find_user_in_room(msgArray[1], room)
        room.banList.append(userBan.name)

        userBan.connection.sendall(("You got banned from " + room.name).encode())

        join_room("#Geral", userBan)

        warningMSG = "User {} was banned from this room".format(userBan.name)
        for users in room.userList:
            users.connection.sendall(warningMSG.encode())

    # give mod to another person
    elif msgArray[0] == "/givemod":
        room = find_chatroom(client.currentRoom)

        if is_mod_in_room(client, room):
            target = find_user_in_room(msgArray[1], room)
            print(target)
            room.moderator.append(target.name)
            target.connection.sendall(("Congratulations!!! You are a mod in " + room.name).encode())

        else:
            client.connection.sendall("You don't have permission in this room".encode())

    # send a private message to a user
    elif msgArray[0] == "/whisper":
        try:
            target = find_user(msgArray[1])
            if target is None:
                client.connection.sendall("")
            else:
                str = "{} whispers: ".format(client.name)
                for x in msgArray[2:]:
                    str += x + " "
                target.connection.sendall(str.encode())
        except IndexError as error:
            client.connection.sendall("It need's a second argument".encode())

    # list's all the available rooms
    elif msgArray[0] == "/list":
        str = "List of Rooms:\n"
        for room in roomList:
            str += room.__str__() + "\n"
        client.connection.sendall(str.encode())

    # list's all the online users
    elif msgArray[0] == "/userlist":
        str = "User list: \n"
        for room in roomList:
            for user in room.userList:
                str += user.__str__() + "\n"
        client.connection.sendall(str.encode())

    # Send a mensage to all the user's in the server (Super Mod)
    elif msgArray[0] == "/broadcast":

        isSuperMod = False
        str = "BROADCAST: "
        # make the message
        for c in msgArray[1:]:
            str += c + " "
        # Broadcast the message if the user is the super mod
        for supmod in superAdminList:
            if supmod == client.name:
                isSuperMod = True
                continue

        if not isSuperMod:
            raise ValueError("You are not super mod")

        # Send the message to every user in every room
        for room in roomList:
            for users in room.userList:
                users.connection.sendall(str.encode())

    # exit command
    elif msgArray[0] == "/exit":
        return "exit function"

    return "function action"


# create the first room
roomList = [ChatRoom("#Geral", "No One")]

superAdminList = ["JonesVentura"]

# Define socket host and port
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 8000

# Create socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.listen(1)
print('Listening on port %s ...' % SERVER_PORT)

username = ""

while True:
    # Wait for client connections
    client_connection, client_address = server_socket.accept()

    # Waiting for the username
    while username == "":
        if find_user(client_connection.recv(1024).decode()) is not None:
            username = client_connection.recv(1024).decode()

    client = Client(username, client_connection)
    if username == "JonesVentura":
        client_connection.sendall("You are a super Admin".encode())

    msg = "You are now connected, {}!".format(username)
    client_connection.sendall(msg.encode())
    client_connection.sendall("You are in #Geral".encode())

    # Send for all the user in the room
    for user in roomList[0].userList:
        msgSend = "User {} has appeared".format(username)
        user.connection.sendall(msgSend.encode())

    # Join the #Geral room
    roomList[0].userList.append(client)

    # Create a thread to accommodate the client
    thread = threading.Thread(target=handle_client, args=(client, ))

    thread.start()

# Close socket
server_socket.close()
