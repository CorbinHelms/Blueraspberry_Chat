import tkinter as tk
from tkinter import messagebox, simpledialog
from chat import BluetoothChat

class ChatGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("600x500")
        self.window.title("Bluetooth Chat")

        self.server_button = tk.Button(self.window, text="Start As Server", bg="#b6d0e2", width=11, height=2, command=self.start_as_server)
        self.server_button.place(x=10, y=20)

        self.client_button = tk.Button(self.window, text="Start As Client", bg="#b6d0e2", width=11, height=2, command=self.connect_client)
        self.client_button.place(x=140, y=20)

        self.incoming_message_box = tk.Text(self.window, bg="white", state="disabled", width=57, height=13)
        self.incoming_message_box.place(x=10, y=90)

        self.outgoing_message_bar = tk.Entry(self.window, width=46)
        self.outgoing_message_bar.place(x=10, y=380)

        self.send_button = tk.Button(self.window, text="Send", bg="#b6d0e2", width=11, height=2, command=self.send_message)
        self.send_button.place(x=480, y=380)

        self.disconnect_button = tk.Button(self.window, text="Disconnect", bg="#d84563", width=11, height=2, command=self.disconnect)
        self.disconnect_button.place(x=480, y=440)

        self.chat = None

        self.window.mainloop()

    def start_as_server(self):
        self.chat = BluetoothChat()
        self.chat.start_as_server()
        messagebox.showinfo("Information", "Server started. Waiting for connection...")

    def connect_client(self):
        server_address = simpledialog.askstring("Input", "Enter server MAC address:")
        self.chat = BluetoothChat(server_address)
        self.chat.connect_client()
        messagebox.showinfo("Information", "Connecting to " + server_address)

    def send_message(self):
        if self.chat:
            message = self.outgoing_message_bar.get()
            self.incoming_message_box.configure(state="normal")
            self.incoming_message_box.insert("end", "You: " + message + "\n")
            self.incoming_message_box.configure(state="disabled")
            self.outgoing_message_bar.delete(0, "end")
            self.chat.send_message(message)

    def display_received_message(self, message):
        self.incoming_message_box.configure(state="normal")
        self.incoming_message_box.insert("end", "Other: " + message + "\n")
        self.incoming_message_box.configure(state="disabled")

    def disconnect(self):
        if self.chat:
            self.chat.disconnect()
            messagebox.showinfo("Information", "Disconnected from Bluetooth device.")
        else:
            messagebox.showinfo("Information", "Not currently connected to a Bluetooth device.")

if __name__ == "__main__":
    ChatGUI()
