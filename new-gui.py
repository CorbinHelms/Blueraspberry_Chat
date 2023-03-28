import tkinter as tk
from tkinter import messagebox, simpledialog
from chat import BluetoothChat

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bluetooth Chat")
        master.geometry("600x500")

        self.incoming_frame = tk.Frame(master, bg="#b6d0e2")
        self.incoming_frame.place(x=10, y=90, width=572, height=261)

        self.incoming_message = tk.Text(self.incoming_frame, bg="#ffffff")
        self.incoming_message.place(relwidth=1, relheight=1)

        self.outgoing_frame = tk.Frame(master, bg="#b6d0e2")
        self.outgoing_frame.place(x=10, y=380, width=461, height=32)

        self.outgoing_message = tk.Entry(self.outgoing_frame, bg="#ffffff")
        self.outgoing_message.place(relwidth=0.8, relheight=1)

        self.send_button = tk.Button(self.outgoing_frame, text="Send", bg="#b6d0e2", command=self.send_message)
        self.send_button.place(relx=0.8, relheight=1, relwidth=0.2)

        self.disconnect_button = tk.Button(master, text="Disconnect", bg="#d84563", command=self.disconnect)
        self.disconnect_button.place(x=480, y=440, width=111, height=32)

        self.start_as_server_button = tk.Button(master, text="Start As Server", bg="#b6d0e2", command=self.start_as_server)
        self.start_as_server_button.place(x=10, y=20, width=111, height=32)

        self.start_as_client_button = tk.Button(master, text="Start As Client", bg="#b6d0e2", command=self.connect_client)
        self.start_as_client_button.place(x=140, y=20, width=111, height=32)

    def start_as_server(self):
        self.chat = BluetoothChat('server')
        self.chat.start_server()
        messagebox.showinfo("Information", "Started as server")

    def connect_client(self):
        server_address = tk.simpledialog.askstring("Input", "Enter server MAC address:")
        messagebox.showinfo("Information", "Connecting to " + server_address)
        self.chat = BluetoothChat('client')
        self.chat.connect_client(server_address)

    def send_message(self):
        message = self.outgoing_message.get()
        self.chat.send_message(message)
        self.outgoing_message.delete(0, 'end')

    def receive_message(self, message):
        self.incoming_message.insert('end', message + "\n")

    def disconnect(self):
        self.chat.disconnect()
        messagebox.showinfo("Information", "Disconnected")


if __name__ == "__main__":
    root = tk.Tk()
    chat_gui = ChatGUI(root)
    root.mainloop()
