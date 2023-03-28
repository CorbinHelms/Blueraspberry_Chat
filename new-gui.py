import tkinter as tk
from tkinter import messagebox, simpledialog
from chat import BluetoothChat

class ChatGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Bluetooth Chat")
        self.master.geometry("600x500")
        self.create_widgets()
        self.chat = None
        
    def create_widgets(self):
        self.incoming_message_box = tk.Text(self.master, width=65, height=15, state="disabled")
        self.incoming_message_box.place(x=10, y=90)
        
        self.outgoing_message_bar = tk.Entry(self.master, width=55)
        self.outgoing_message_bar.place(x=10, y=380)
        
        self.start_as_server_button = tk.Button(self.master, text="Start As Server", width=20, height=2, bg="#b6d0e2", command=self.start_as_server)
        self.start_as_server_button.place(x=10, y=20)
        
        self.start_as_client_button = tk.Button(self.master, text="Start As Client", width=20, height=2, bg="#b6d0e2", command=self.connect_client)
        self.start_as_client_button.place(x=140, y=20)
        
        self.send_button = tk.Button(self.master, text="Send", width=20, height=2, bg="#b6d0e2", command=self.send_message)
        self.send_button.place(x=480, y=380)
        
        self.disconnect_button = tk.Button(self.master, text="Disconnect", width=20, height=2, bg="#d84563", command=self.disconnect)
        self.disconnect_button.place(x=480, y=440)

    def start_as_server(self):
        self.chat = BluetoothChat()
        self.chat.start_server()
        self.incoming_message_box.config(state="normal")
        self.incoming_message_box.insert("end", "Server started...\n")
        self.incoming_message_box.config(state="disabled")
        
    def connect_client(self):
        server_address = simpledialog.askstring("Input", "Enter server MAC address:")
        self.chat = BluetoothChat()
        self.chat.connect_client(server_address)
        self.incoming_message_box.config(state="normal")
        self.incoming_message_box.insert("end", "Connected to server " + server_address + "\n")
        self.incoming_message_box.config(state="disabled")
        
    def send_message(self):
        message = self.outgoing_message_bar.get()
        self.outgoing_message_bar.delete(0, "end")
        self.chat.send_message(message)
        self.incoming_message_box.config(state="normal")
        self.incoming_message_box.insert("end", "You: " + message + "\n")
        self.incoming_message_box.config(state="disabled")
        
    def disconnect(self):
        self.chat.disconnect()
        self.incoming_message_box.config(state="normal")
        self.incoming_message_box.insert("end", "Disconnected from server\n")
        self.incoming_message_box.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(master=root)
    app.mainloop()
