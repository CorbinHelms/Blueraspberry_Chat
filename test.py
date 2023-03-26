import os
import sys
import bluetooth
import threading
import tkinter as tk
from tkinter import messagebox


class Chat:
    def __init__(self, is_server):
        self.server_sock = None
        self.client_sock = None
        self.is_server = is_server
        self.running = False

        # If running as a server, wait for client to connect
        if self.is_server:
            self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.server_sock.bind(("", bluetooth.PORT_ANY))
            self.server_sock.listen(1)
            self.port = self.server_sock.getsockname()[1]

            messagebox.showinfo("Server", "Waiting for client to connect...")

            self.client_sock, self.client_info = self.server_sock.accept()
            messagebox.showinfo("Server", "Client connected!")
        else:
            # If running as a client, connect to server
            server_address = input("Enter server MAC address: ")
            self.client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

            try:
                self.client_sock.connect((server_address, bluetooth.PORT_ANY))
                messagebox.showinfo("Client", "Connected to server!")
            except bluetooth.btcommon.BluetoothError as err:
                messagebox.showerror("Client", f"Error: {err}")
                sys.exit()

        # Start the thread to receive messages
        threading.Thread(target=self.receive_messages).start()

    def send_message(self, message):
        if self.running:
            self.client_sock.send(message.encode())
            print("Message sent")
        else:
            print("Error: client not connected")

    def receive_messages(self):
        self.running = True

        while self.running:
            try:
                message = self.client_sock.recv(1024).decode()
                print(f"Received message: {message}")
                self.gui.add_message(message)
            except bluetooth.btcommon.BluetoothError as err:
                print(f"Error: {err}")
                self.running = False

        self.client_sock.close()
        self.server_sock.close()

    def disconnect(self):
        self.running = False


class ChatGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Bluetooth Chat")
        
        self.connection_frame = tk.Frame(self.root)
        self.connection_frame.pack(pady=10)
        
        self.server_button = tk.Button(self.connection_frame, text="Start as Server", command=self.start_server)
        self.server_button.pack(side=tk.LEFT, padx=5)
        
        self.client_button = tk.Button(self.connection_frame, text="Start as Client", command=self.start_client)
        self.client_button.pack(side=tk.LEFT, padx=5)
        
        self.root.mainloop()
    
    def start_server(self):
        chat = Chat(is_server=True)
        self.display_chat(chat)
        
    def start_client(self):
        chat = Chat(is_server=False)
        self.display_chat(chat)
        
    def display_chat(self, chat):
        self.root.withdraw()
        self.gui = ChatGUIWindow(chat, self.root)
        
        
class ChatGUIWindow:
    def __init__(self, chat, master=None):
        self.chat = chat
        
        self.chat_frame = tk.Frame(master)
        self.chat_frame.pack(padx=10, pady=10)
        
        self.message_entry = tk.Entry(self.chat_frame)
        self.message_entry.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        
def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
