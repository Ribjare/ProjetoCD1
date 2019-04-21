"""
 Implements a simple socket client

"""
import socket
import threading
from tkinter import*
import tkinter as tk
import tkinter.font

isDeactive = False
n = 0
username = ""


class Client(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.setting_user_name()

    def return_self(self):
        return self

    # cria os widgets
    def create_widgets(self):
        bot_frame = tk.Frame(self)
        top_frame = tk.Frame(self)
        bot_frame.pack(side=BOTTOM)
        top_frame.pack(side=TOP)

        font = tk.font.Font(size=14)

        self.mensagem_text_box = Listbox(top_frame, width=65, height=25, font=font)
        self.chat_room_text_box = Listbox(top_frame, width=40, height=30)
        self.members_text_box = Listbox(top_frame, width=40, height=30)

        self.chat_room_text_box.insert(0, "#Geral")

        self.text = StringVar()
        self.message = tk.Entry(bot_frame, textvariable=self.text, width=110)
        self.send_msg = tk.Button(bot_frame)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.quit_function)
        self.display_widgets()

    def quit_function(self):
        send_msg("/exit")
        self.master.destroy()

    # Organiza os widgets usados
    def display_widgets(self):
        self.send_msg["text"] = "Send"
        self.send_msg["command"] = self.send_msgs
        self.display_server_messages()

        self.send_msg.pack(side=RIGHT)

        self.chat_room_text_box.pack(side=LEFT)

        self.message.pack(side=LEFT, padx=10)

        self.mensagem_text_box.pack(side=LEFT, pady=10, padx=10)

        self.members_text_box.pack(side=RIGHT)

        self.quit.pack(side=BOTTOM)

        self.add_chatroom_name("")
        self.add_user("")

    # corta a mensagem, se for demasiado longa
    def cut_message(self, msg):
        msgArray = msg.split()
        txt_1 = ""
        txt_2 = ""
        n = 0
        for i in msgArray:
            if n <= 10:
                txt_1 += i + " "
            if n > 10:
                txt_2 += i + " "
            n += 1
        return txt_1, txt_2

    # envia a mensagem escrita para o chat
    def send_msgs(self):
        send_msg(self.text.get())
        if self.text.get() != "":
            if self.text.get().__sizeof__() >= 20:
                cut_text = self.cut_message(self.text.get())
                self.mensagem_text_box.insert(self.mensagem_text_box.size(), cut_text[0])
                self.mensagem_text_box.insert(self.mensagem_text_box.size(), cut_text[1])
        self.message.delete(0, 'end')

    # mensagens
    def display_server_messages(self):
        if n == 0:
            self.mensagem_text_box.insert(self.mensagem_text_box.size(), "$ Username?")

    def setting_user_name(self):
        username = self.mensagem_text_box.get(1)
        print(username)

    # envia mensagens do server
    def recive_msgs_from_server(self, msg):
        if msg == "":
            return

        split = msg.split(" ")
        if len(split) >=2:
            if split[1] == "room" and split[4] == "created":
                self.add_chatroom_name(split[2])

        if msg.__sizeof__() >= 20:
            if "(" not in msg[1]:
                cut_text = msg.split("\n")
                for m in cut_text:
                    self.mensagem_text_box.insert(self.mensagem_text_box.size(), m)
            else:
                cut_text = self.cut_message(msg)
                for text in cut_text:
                    self.mensagem_text_box.insert(self.mensagem_text_box.size(), text)
        else:
            self.mensagem_text_box.insert(self.mensagem_text_box.size(), msg)

    # adiciona um utilizador à lista
    def add_user(self, name):
        self.members_text_box.insert(self.members_text_box.size(), "Bob")
        if name != "":
            self.members_text_box.insert(self.members_text_box.size(), "#" + name)

    # adiciona um chatroom à lista
    def add_chatroom_name(self, name):

        if name != "":
            self.chat_room_text_box.insert(self.chat_room_text_box.size(), name)


# Receives from the server and handle them
def handle_msg(self):
    while True:
        if isDeactive:
            break
        # Read answer
        res = client_socket.recv(1024).decode()
        print(res)
        app.recive_msgs_from_server(res)


def send_msg(msg):
    client_socket.sendall(msg.encode())


# Initializes the interface
root = Tk()
root.geometry("1250x680")
root.resizable(0, 0)
root.title("Chat Service")
app = Client(root)


# Define socket host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 8000

# Create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server
client_socket.connect((SERVER_HOST, SERVER_PORT))


# Create a thread to receive msg
thread = threading.Thread(target=handle_msg, args=(client_socket, ))
thread.start()

# Starts the interface
app.mainloop()

# Close socket
client_socket.close()





