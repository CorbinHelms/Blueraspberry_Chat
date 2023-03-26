import tkinter as tk
from tkinter import scrolledtext
import bluetooth

class ChatGUI:
    def __init__(self, master):
        self.master = master
        master.title("Bluetooth Chat")
        master.configure(background='#1E90FF')
        master.resizable(False, False)

        self.frame = tk.Frame(master, background='#B0E0E6')
        self.frame.pack(padx=10, pady=10)

        self.chat_log = scrolledtext.ScrolledText(self.frame, width=40, height=10)
        self.chat_log.configure(state='disabled')
        self.chat_log.grid(row=0, column=0, padx=5, pady=5)

        self.entry_field = tk.Entry(self.frame, width=30)
        self.entry_field.grid(row=1, column=0, padx=5, pady=5)

        self.send_button = tk.Button(self.frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, padx=5, pady=5)

        self.quit_button = tk.Button(self.frame, text="Quit", command=self.master.quit)
        self.quit_button.grid(row=1, column=2, padx=5, pady=5)

    def send_message(self):
        message = self.entry_field.get()
        if message:
            self.entry_field.delete(0, tk.END)
            self.chat_log.configure(state='normal')
            self.chat_log.insert(tk.END, f"You: {message}\n")
            self.chat_log.see(tk.END)
            self.chat_log.configure(state='disabled')
            send_message_to_server(message)

    def display_message(self, message):
        self.chat_log.configure(state='normal')
        self.chat_log.insert(tk.END, f"Server: {message}\n")
        self.chat_log.see(tk.END)
        self.chat_log.configure(state='disabled')
        
server_address = None
client_socket = None

def connect_to_server():
    global server_address, client_socket
    nearby_devices = bluetooth.discover_devices()
    for device in nearby_devices:
        if 'Raspberry Pi' in bluetooth.lookup_name(device):
            server_address = device
            break

    if server_address is None:
        print("No nearby Raspberry Pi devices found.")
        return False

    port = 1
    client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_socket.connect((server_address, port))
    return True

def close_connection():
    if client_socket:
        client_socket.close()

def send_message_to_server(message):
    if client_socket:
        client_socket.send(message.encode())

def receive_messages_from_server(chat_gui):
    while True:
        if client_socket:
            message = client_socket.recv(1024)
            if message:
                chat_gui.display_message(message.decode())
                
if __name__ == '__main__':
    root = tk.Tk()
    chat_gui = ChatGUI(root)
    connected = connect_to_server()
    if connected:
        receive_thread = threading.Thread(target=receive_messages_from_server, args=(chat_gui,))
