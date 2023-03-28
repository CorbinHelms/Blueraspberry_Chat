import tkinter as tk
from tkinter import messagebox, simpledialog
from chat import BluetoothChat

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("600x500")
        self.master.title("Bluetooth Chat")

        self.incoming_messages = tk.Text(master, width=71, height=14, wrap=tk.WORD)
        self.incoming_messages.place(x=10, y=90)

        self.outgoing_message = tk.Entry(master, width=60)
        self.outgoing_message.place(x=10, y=380)

        self.send_button = tk.Button(master, text="Send", width=11, height=1, bg="#b6d0e2", command=self.send_message)
        self.send_button.place(x=480, y=380)

        self.disconnect_button = tk.Button(master, text="Disconnect", width=11, height=1, bg="#d84563", command=self.disconnect)
        self.disconnect_button.place(x=480, y=440)

        self.start_server_button = tk.Button(master, text="Start As Server", width=11, height=1, bg="#b6d0e2", command=self.start_server)
        self.start_server_button.place(x=10, y=20)

        self.start_client_button = tk.Button(master, text="Start As Client", width=11, height=1, bg="#b6d0e2", command=self.connect_client)
        self.start_client_button.place(x=140, y=20)

    def send_message(self):
        message = self.outgoing_message.get()
        if message:
            self.incoming_messages.insert(tk.END, "You: " + message + "\n")
            self.outgoing_message.delete(0, tk.END)
            self.chat.send(message)

    def update_messages(self, message):
        self.incoming_messages.insert(tk.END, "Partner: " + message + "\n")

    def start_server(self):
        self.chat = BluetoothChat()
        self.chat.start_server()
        self.master.after(500, self.check_for_messages)

    def connect_client(self):
        server_address = simpledialog.askstring("Input", "Enter server MAC address:")
        messagebox.showinfo("Information", "Connecting to " + server_address)
        self.chat = BluetoothChat(server_address)
        self.chat.connect_client(server_address)
        self.master.after(500, self.check_for_messages)

    def check_for_messages(self):
        message = self.chat.get_message()
        if message:
            self.update_messages(message)
        self.master.after(500, self.check_for_messages)

    def disconnect(self):
        self.chat.disconnect()
        self.incoming_messages.delete(1.0, tk.END)
        self.outgoing_message.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
