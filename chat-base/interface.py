from tkinter import*
import tkinter as tk
import tkinter.font


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def write_message(self):
        return self.text

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

        self.text = StringVar()
        self.message = tk.Entry(bot_frame, textvariable=self.text, width=110)
        self.send_msg = tk.Button(bot_frame)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.display_widgets()

    # Organiza os widgets usados
    def display_widgets(self):
        self.send_msg["text"] = "Send"
        self.send_msg["command"] = self.send_msgs

        self.send_msg.pack(side=RIGHT)

        self.chat_room_text_box.pack(side=LEFT)

        self.message.pack(side=LEFT, padx=10)

        self.mensagem_text_box.pack(side=LEFT, pady=10, padx=10)

        self.members_text_box.pack(side=RIGHT)

        self.quit.pack(side=BOTTOM)

    # envia a mensagem escrita para o chat
    def send_msgs(self):
        print(format(self.text))
        if self.text.get() != "":
            self.mensagem_text_box.insert(2, "" + self.text.get())
        self.message.delete(0, 'end')


root = tk.Tk()
root.geometry("1250x680")
root.resizable(0,0)
app = Application(master=root)
app.mainloop()