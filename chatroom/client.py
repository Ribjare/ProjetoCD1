"""
 Implements a simple socket client

"""
import socket
import threading
if __name__ == '__main__':
    from chatroom.interface import Application


isDeactive = False


# Receives from the server and handle them
def handle_msg(client):
    while True:
        if isDeactive:
            break
        # Read answer
        res = client.recv(1024).decode()
        print(res)


def send_message():
    msg = Application.send_message_to_user()
    client_socket.sendall(msg.encode())
    return msg


# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((SERVER_HOST, SERVER_PORT))

# First connection send username
print("$ Username?")
# msg = interface.write_message
# msg = input('> ')
mens = send_message()
client_socket.sendall(mens.encode())
res = client_socket.recv(1024).decode()
print(res)
# Create a thread to receive msg
thread = threading.Thread(target=handle_msg, args=(client_socket, ))
thread.start()

# Next msg
while True:

    # Send message
    # msg = input("")
    mens = send_message()
    client_socket.sendall(mens.encode())

    # Check for exit
    if msg == '/exit':
        res = client_socket.recv(1024).decode()
        print(res)
        isDeactive = True
        break




# Close socket
client_socket.close()
