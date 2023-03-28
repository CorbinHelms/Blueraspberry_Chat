import tkinter as tk
from tkinter import messagebox, simpledialog
from chat import BluetoothChat

class ChatGUI(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.title("Bluetooth Chat")
        self.geometry("600x500")
        self.resizable(False, False)

        # Create widgets
        self.server_button = tk.Button(self, text="Start As Server", command=self.start_as_server, bg="#b6d0e2", width=111, height=32)
        self.server_button.place(x=10, y=20)

        self.client_button = tk.Button(self, text="Start As Client", command=self.connect_client, bg="#b6d0e2", width=111, height=32)
        self.client_button.place(x=140, y=20)

        self.incoming_text = tk.Text(self, width=57, height=26)
        self.incoming_text.place(x=10, y=90)

        self.outgoing_entry = tk.Entry(self, width=46)
        self.outgoing_entry.place(x=10, y=380)

        self.send_button = tk.Button(self, text="Send", command=self.send_message, bg="#b6d0e2", width=111, height=32)
        self.send_button.place(x=480, y=380)

        self.disconnect_button = tk.Button(self, text="Disconnect", command=self.disconnect, bg="#d84563", width=111, height=32)
        self.disconnect_button.place(x=480, y=440)

    def start_as_server(self):
        self.chat = BluetoothChat()
        self.chat.start_server()
        messagebox.showinfo("Information", "Server started")

    def connect_client(self):
        server_address = tk.simpledialog.askstring("Input", "Enter server MAC address:")
        messagebox.showinfo("Information", "Connecting to " + server_address)
        self.chat = BluetoothChat()
        self.chat.connect_client(server_address)

    def send_message(self):
        message = self.outgoing_entry.get()
        self.chat.send(message)
        self.incoming_text.insert(tk.END, "Me: " + message + "\n")
        self.outgoing_entry.delete(0, tk.END)

    def disconnect(self):
        self.chat.disconnect()
        messagebox.showinfo("Information", "Disconnected")

if __name__ == "__main__":
    gui = ChatGUI()
    gui.mainloop()
