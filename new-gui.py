import tkinter as tk
from tkinter import messagebox, simpledialog
from chat import BluetoothChat

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bluetooth Chat")
        master.geometry("600x500")
        
        # Incoming message box
        self.incoming_messages = tk.Text(master, width=71, height=13)
        self.incoming_messages.configure(state='disabled')
        self.incoming_messages.place(x=10, y=90)

        # Outgoing message bar
        self.outgoing_message = tk.Entry(master, width=58)
        self.outgoing_message.place(x=10, y=380)

        # Send button
        self.send_button = tk.Button(master, text="Send", width=12, height=2, bg="#b6d0e2", command=self.send_message)
        self.send_button.place(x=480, y=380)

        # Disconnect button
        self.disconnect_button = tk.Button(master, text="Disconnect", width=12, height=2, bg="#d84563", command=self.disconnect)
        self.disconnect_button.place(x=480, y=440)

        # Start as server button
        self.start_as_server_button = tk.Button(master, text="Start as Server", width=12, height=2, bg="#b6d0e2", command=self.start_as_server)
        self.start_as_server_button.place(x=10, y=20)

        # Start as client button
        self.start_as_client_button = tk.Button(master, text="Start as Client", width=12, height=2, bg="#b6d0e2", command=self.connect_client)
        self.start_as_client_button.place(x=140, y=20)
        
        self.chat = None
        
    def start_as_server(self):
        if self.chat is not None:
            messagebox.showwarning("Warning", "Already connected to a device.")
            return

        self.chat = BluetoothChat()
        self.chat.start_server()
        
    def connect_client(self):
        if self.chat is not None:
            messagebox.showwarning("Warning", "Already connected to a device.")
            return

        server_address = tk.simpledialog.askstring("Input", "Enter server MAC address:")
        if server_address is not None:
            self.chat = BluetoothChat(server_address)
            self.chat.connect_client(server_address)
            messagebox.showinfo("Information", "Connecting to " + server_address)
            
    def send_message(self):
        if self.chat is not None:
            message = self.outgoing_message.get()
            self.chat.send(message)
            self.incoming_messages.configure(state='normal')
            self.incoming_messages.insert('end', "Me: " + message + "\n")
            self.incoming_messages.configure(state='disabled')
            self.outgoing_message.delete(0, 'end')
        else:
            messagebox.showwarning("Warning", "Not connected to a device.")
            
    def disconnect(self):
        if self.chat is not None:
            self.chat.disconnect()
            self.chat = None
            messagebox.showinfo("Information", "Disconnected from device.")
        else:
            messagebox.showwarning("Warning", "Not connected to a device.")
        
root = tk.Tk()
gui = ChatGUI(root)
root.mainloop()
