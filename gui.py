import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from chat import BluetoothChat
import threading
import sys


class ChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bluetooth Chat")
        self.root.geometry("600x500")

        self.incoming_frame = tk.LabelFrame(self.root, text="Incoming Messages", width=572, height=261)
        self.incoming_frame.place(x=10, y=90)

        self.outgoing_message = tk.Entry(self.root, width=53)
        self.outgoing_message.place(x=10, y=380)

        self.send_button = tk.Button(self.root, text="Send", bg="#b6d0e2", width=10, height=1, command=self.send_message)
        self.send_button.place(x=480, y=380)

        self.disconnect_button = tk.Button(self.root, text="Disconnect", bg="#d84563", width=10, height=1, command=self.disconnect)
        self.disconnect_button.place(x=480, y=440)

        self.start_server_button = tk.Button(self.root, text="Start as Server", bg="#b6d0e2", width=10, height=1, command=self.start_as_server)
        self.start_server_button.place(x=10, y=20)

        self.start_client_button = tk.Button(self.root, text="Start as Client", bg="#b6d0e2", width=10, height=1, command=self.start_as_client)
        self.start_client_button.place(x=140, y=20)

        self.chat = None
        self.thread = None

    def send_message(self):
        message = self.outgoing_message.get().strip()
        if message:
            self.outgoing_message.delete(0, tk.END)
            self.thread = threading.Thread(target=self.chat.send_message, args=(message,))
            self.thread.start()

    def disconnect(self):
        if self.chat:
            self.thread = threading.Thread(target=self.chat.disconnect)
            self.thread.start()

    def start_as_server(self):
        self.chat = BluetoothChat()
        self.thread = threading.Thread(target=self.chat.start_server)
        self.thread.start()

    def connect_client(self):
        server_address = tk.simpledialog.askstring("Input", "Enter server MAC address:")
        if server_address:
            messagebox.showinfo("Information", "Connecting to " + server_address)
            self.chat = BluetoothChat()
            self.thread = threading.Thread(target=self.chat.connect_client, args=(server_address,))
            self.thread.start()

    def start_as_client(self):
        self.connect_client()

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    chat_gui = ChatGUI()
    chat_gui.run()
