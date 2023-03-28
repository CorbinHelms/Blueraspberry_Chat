import tkinter as tk
from tkinter import messagebox, simpledialog
from chat import BluetoothChat

class ChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Bluetooth Chat")
        self.chat = None

        self.incoming_frame = tk.Frame(self.master, width=572, height=261, bd=1, relief=tk.RIDGE)
        self.incoming_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.incoming_text = tk.Text(self.incoming_frame, state=tk.DISABLED, wrap=tk.WORD)
        self.incoming_text.pack(fill=tk.BOTH, expand=True)

        self.outgoing_frame = tk.Frame(self.master, width=461, height=32, bd=1, relief=tk.RIDGE)
        self.outgoing_frame.grid(row=1, column=0, padx=10, pady=10)
        self.outgoing_label = tk.Label(self.outgoing_frame, text="Message: ")
        self.outgoing_label.pack(side=tk.LEFT)
        self.outgoing_entry = tk.Entry(self.outgoing_frame, width=50)
        self.outgoing_entry.pack(side=tk.LEFT)

        self.server_button = tk.Button(self.master, text="Start as Server", width=15, height=2, bg="#b6d0e2", command=self.start_as_server)
        self.server_button.grid(row=2, column=0, padx=10, pady=10)

        self.client_button = tk.Button(self.master, text="Start as Client", width=15, height=2, bg="#b6d0e2", command=self.connect_client)
        self.client_button.grid(row=2, column=1, padx=10, pady=10)

        self.send_button = tk.Button(self.master, text="Send", width=15, height=2, bg="#b6d0e2", command=self.send_message)
        self.send_button.grid(row=2, column=2, padx=10, pady=10)

        self.disconnect_button = tk.Button(self.master, text="Disconnect", width=15, height=2, bg="#d84563", command=self.disconnect)
        self.disconnect_button.grid(row=2, column=3, padx=10, pady=10)
        
    def start_as_server(self):
        self.chat = BluetoothChat()
        self.chat.start_as_server()
        messagebox.showinfo("Information", "Started as server")

    def connect_client(self):
        server_address = simpledialog.askstring("Input", "Enter server MAC address:")
        if server_address:
            self.chat = BluetoothChat()
            self.chat.connect_client(server_address)
            messagebox.showinfo("Information", "Connecting to " + server_address)

    def send_message(self):
        if self.chat:
            message = self.outgoing_entry.get()
            if message:
                self.chat.send_message(message)
                self.outgoing_entry.delete(0, tk.END)
                self.incoming_text.config(state=tk.NORMAL)
                self.incoming_text.insert(tk.END, "Me: " + message + "\n")
                self.incoming_text.config(state=tk.DISABLED)

    def disconnect(self):
        if self.chat:
            self.chat.disconnect()
            messagebox.showinfo("Information", "Disconnected")
            self.chat = None

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatGUI(root)
    root.mainloop()
