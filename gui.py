import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from chat import BluetoothChat
import threading
import sys


class BluetoothChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bluetooth Chat")
        self.root.geometry("600x500")

        self.incoming_frame = tk.LabelFrame(self.root, text="Incoming Messages", width=572, height=261)
        self.incoming_frame.place(x=10, y=90)

        self.outgoing_message = tk.Entry(self.root, width=48)
        self.outgoing_message.place(x=10, y=380, width=461, height=32)

        self.send_button = tk.Button(self.root, text="Send", bg="#b6d0e2", width=10, height=1, command=self.send_message)
        self.send_button.place(x=481, y=380, width=111, height=32)

        self.disconnect_button = tk.Button(self.root, text="Disconnect", bg="#d84563", width=10, height=1, command=self.disconnect)
        self.disconnect_button.place(x=481, y=440, width=111, height=32)

        self.start_server_button = tk.Button(self.root, text="Start as Server", bg="#b6d0e2", width=10, height=1, command=self.start_as_server)
        self.start_server_button.place(x=10, y=20, width=111, height=32)

        self.start_client_button = tk.Button(self.root, text="Start as Client", bg="#b6d0e2", width=10, height=1, command=self.start_as_client)
        self.start_client_button.place(x=140, y=20, width=111, height=32)

        self.chat = None
        self.thread = None

    def start_server(self):
        self.chat = BluetoothChat()
        self.chat.start_server()
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.start()

    def start_client(self):
        server_mac_address = self.client_entry.get()
        self.chat = BluetoothChat()
        self.chat.start_client(server_mac_address)
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.start()

    def receive_message(self):
        while True:
            data = self.chat.client_sock.recv(1024)
            if not data:
                break
        self.receive_text.config(state="normal")
        self.receive_text.insert(tk.END, data.decode("utf-8"))
        self.receive_text.see(tk.END)
        self.receive_text.config(state="disabled")

        self.receive_text.config(state="normal")
        self.receive_text.insert(tk.END, "Connection closed\n")
        self.receive_text.config(state="disabled")

    def send_message(self):
        message = self.outgoing_entry.get()
        self.chat.client_sock.send(message.encode("utf-8"))
        self.outgoing_entry.delete(0, tk.END)

    def close(self):
        self.chat.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothChatGUI(master=root)
    app.mainloop()
