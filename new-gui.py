import tkinter as tk
from tkinter import simpledialog, messagebox
from chat import BluetoothChat

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bluetooth Chat")
        master.geometry("600x500")
        master.resizable(False, False)

        self.incoming_frame = tk.Frame(master, width=572, height=261, bd=2, relief="sunken")
        self.incoming_frame.place(x=10, y=90)
        self.incoming_text = tk.Text(self.incoming_frame, state="disabled", font=("Courier New", 10))
        self.incoming_text.place(x=2, y=2, width=568, height=257)

        self.outgoing_bar = tk.Entry(master, width=60)
        self.outgoing_bar.place(x=10, y=380, width=461, height=32)
        self.outgoing_bar.bind("<Return>", self.send_message)

        self.start_server_button = tk.Button(master, text="Start As Server", command=self.start_server, bg="#b6d0e2", width=11, height=1)
        self.start_server_button.place(x=10, y=20)

        self.start_client_button = tk.Button(master, text="Start As Client", command=self.connect_client, bg="#b6d0e2", width=11, height=1)
        self.start_client_button.place(x=140, y=20)

        self.send_button = tk.Button(master, text="Send", command=self.send_message, bg="#b6d0e2", width=11, height=1)
        self.send_button.place(x=480, y=380)

        self.disconnect_button = tk.Button(master, text="Disconnect", command=self.disconnect, bg="#d84563", width=11, height=1)
        self.disconnect_button.place(x=480, y=440)

        self.chat = None

    def start_server(self):
        self.chat = BluetoothChat()
        self.chat.start_server()
        messagebox.showinfo("Information", "Server started")

    def connect_client(self):
        server_address = tk.simpledialog.askstring("Input", "Enter server MAC address:")
        messagebox.showinfo("Information", "Connecting to " + server_address)
        self.chat = BluetoothChat(server_address)
        self.chat.connect_client(server_address)

    def send_message(self, event=None):
        if self.chat is not None:
            message = self.outgoing_bar.get()
            if message.strip() != "":
                self.chat.send_message(message)
                self.outgoing_bar.delete(0, "end")

    def disconnect(self):
        if self.chat is not None:
            self.chat.disconnect()
            self.chat = None
            messagebox.showinfo("Information", "Disconnected")
