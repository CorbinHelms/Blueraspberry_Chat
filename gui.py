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

    def start_as_server(self):
           self.chat = BluetoothChat()
           self.chat.start_server()
           self.thread = threading.Thread(target=self.receive_message)
           self.thread.start()

    def start_as_client(self):
        server_mac_address = simpledialog.askstring("Server MAC Address", "Enter the server's MAC address:")
        if server_mac_address is not None:
            self.chat = BluetoothChat()
            self.chat.start_client(server_mac_address)
            self.thread = threading.Thread(target=self.receive_message)
            self.thread.start()

    def receive_message(self):
        while True:
            data = receive_message(self):
            if data:
                self.incoming_message.configure(state="normal")
                self.incoming_message.insert(tk.END, ">> " + data + "\n")
                self.incoming_message.configure(state="disabled")
            else:
                messagebox.showerror("Error", "Lost connection to server")
                self.disconnect()

    def send_message(self):
        message = self.outgoing_message.get()
        if self.chat.send(message):
            self.incoming_message.configure(state="normal")
            self.incoming_message.insert(tk.END, "<< " + message + "\n")
            self.incoming_message.configure(state="disabled")
            self.outgoing_message.delete(0, tk.END)

    def disconnect(self):
        self.chat.close()
        self.chat = None
        self.thread = None
        self.incoming_message.configure(state="normal")
        self.incoming_message.delete("1.0", tk.END)
        self.incoming_message.configure(state="disabled")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = BluetoothChatGUI()
    gui.run()
