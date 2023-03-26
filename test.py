import tkinter as tk
from tkinter import messagebox
from threading import Thread
import chat

class ServerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Server")
        self.root.geometry("300x200")

        # create buttons
        self.start_btn = tk.Button(root, text="Start as Server", command=self.start_server)
        self.start_btn.pack(pady=20)

    def start_server(self):
        # start server in a new thread
        server_thread = Thread(target=chat.start_server)
        server_thread.start()

        # create new window for chat
        self.chat_window = tk.Toplevel(self.root)
        self.chat_window.title("Chat Window")
        self.chat_window.geometry("400x400")

        # create label for showing connection status
        self.status_label = tk.Label(self.chat_window, text="Waiting for client...")
        self.status_label.pack(pady=10)

        # create text widget for showing chat messages
        self.chat_text = tk.Text(self.chat_window)
        self.chat_text.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        # create entry widget for sending messages
        self.message_entry = tk.Entry(self.chat_window)
        self.message_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=20, pady=10)

        # create send button
        self.send_button = tk.Button(self.chat_window, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=5, pady=10)

        # create disconnect button
        self.disconnect_button = tk.Button(self.chat_window, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(side=tk.RIGHT, padx=20, pady=10)

    def send_message(self):
        message = self.message_entry.get()
        chat.send_message(message)
        self.message_entry.delete(0, tk.END)

    def disconnect(self):
        chat.disconnect()
        self.chat_window.destroy()
        self.start_btn.pack(pady=20)

class ServerGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Server")
        self.master.geometry("400x300")
        self.master.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.frame_top = Frame(self.master)
        self.frame_top.pack(side=TOP, pady=10)

        self.label_status = Label(self.frame_top, text="Press 'Start as Server' to begin", font=("Helvetica", 12))
        self.label_status.pack(side=TOP)

        self.button_start_server = Button(self.frame_top, text="Start as Server", font=("Helvetica", 12), command=self.start_server)
        self.button_start_server.pack(side=TOP, pady=10)

        self.frame_bottom = Frame(self.master)
        self.frame_bottom.pack(side=BOTTOM, pady=10)

        self.text_box = Text(self.frame_bottom, state=DISABLED, font=("Helvetica", 12))
        self.text_box.pack(side=TOP, pady=10)

        self.entry_message = Entry(self.frame_bottom, font=("Helvetica", 12))
        self.entry_message.pack(side=LEFT, padx=10)

        self.button_send = Button(self.frame_bottom, text="Send", font=("Helvetica", 12), command=self.send_message)
        self.button_send.pack(side=LEFT)

        self.button_disconnect = Button(self.frame_bottom, text="Disconnect", font=("Helvetica", 12), command=self.disconnect, state=DISABLED)
        self.button_disconnect.pack(side=RIGHT, padx=10)

    def start_server(self):
        self.server = BluetoothServer(self)
        self.button_start_server.config(state=DISABLED)
        self.entry_message.config(state=NORMAL)
        self.button_send.config(state=NORMAL)
        self.button_disconnect.config(state=NORMAL)
        self.label_status.config(text="Waiting for client...")

    def send_message(self):
        message = self.entry_message.get().strip()
        if message:
            self.server.send(message)
            self.entry_message.delete(0, END)

    def on_receive_message(self, message):
        self.text_box.config(state=NORMAL)
        self.text_box.insert(END, "Client: " + message + "\n")
        self.text_box.config(state=DISABLED)

    def on_client_connected(self):
        self.label_status.config(text="Client connected.")
        self.entry_message.config(state=NORMAL)
        self.button_send.config(state=NORMAL)

    def on_client_disconnected(self):
        self.label_status.config(text="Client disconnected.")
        self.entry_message.config(state=DISABLED)
        self.button_send.config(state=DISABLED)
        self.button_disconnect.config(state=DISABLED)
        self.text_box.config(state=NORMAL)
        self.text_box.delete(1.0, END)
        self.text_box.config(state=DISABLED)

    def disconnect(self):
        self.server.disconnect()
        self.button_start_server.config(state=NORMAL)
        self.entry_message.config(state=DISABLED)
        self.button_send.config(state=DISABLED)
        self.button_disconnect.config(state=DISABLED)
        self.label_status.config(text="Press 'Start as Server' to begin")

    def on_exit(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            if hasattr(self, 'server'):
                self.server.disconnect()
            self.master.destroy()

class ClientGUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.server_mac = None
        self.client_socket = None
        self.receive_thread = None
        self.connected = False

        self.title("Bluetooth Chat Client")

        self.start_frame = tk.Frame(self)
        self.start_frame.pack(padx=20, pady=20)

        self.server_label = tk.Label(self.start_frame, text="Server MAC Address:")
        self.server_label.pack(side=tk.LEFT)

        self.server_entry = tk.Entry(self.start_frame, width=20)
        self.server_entry.pack(side=tk.LEFT)

        self.connect_button = tk.Button(self.start_frame, text="Connect", command=self.connect)
        self.connect_button.pack(side=tk.LEFT)

        self.chat_frame = tk.Frame(self)
        self.chat_frame.pack(padx=20, pady=20)

        self.messages = tk.Text(self.chat_frame, height=15, width=50)
        self.messages.pack(side=tk.TOP, pady=10)

        self.send_frame = tk.Frame(self.chat_frame)
        self.send_frame.pack(side=tk.BOTTOM)

        self.message_entry = tk.Entry(self.send_frame, width=30)
        self.message_entry.pack(side=tk.LEFT, padx=5)

        self.send_button = tk.Button(self.send_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.disconnect_button = tk.Button(self.chat_frame, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(side=tk.BOTTOM, pady=10)

        self.update()

    def connect(self):
        # Get server MAC address from entry
        self.server_mac = self.server_entry.get()
        if not self.server_mac:
            self.messages.insert(tk.END, "Please enter a valid MAC address.\n")
            return

        # Try to connect to server
        self.messages.insert(tk.END, f"Connecting to {self.server_mac}...\n")
        try:
            self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.client_socket.connect((self.server_mac, 1))
        except bluetooth.BluetoothError as e:
            self.messages.insert(tk.END, f"Error connecting to {self.server_mac}: {e}\n")
            return

        # Start receive thread
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

        # Update GUI
        self.connected = True
        self.messages.insert(tk.END, f"Connected to {self.server_mac}.\n")
        self.start_frame.pack_forget()
        self.chat_frame.pack()

    def receive_messages(self):
        while self.connected:
            try:
                message = self.client_socket.recv(1024).decode()
                self.messages.insert(tk.END, f"Server: {message}")
            except bluetooth.BluetoothError as e:
                self.messages.insert(tk.END, f"Error receiving message: {e}\n")
                break

        # Create the frame for the client GUI
        self.client_frame = Frame(self.root)

        # Create the input box and send button
        self.client_input_box = Entry(self.client_frame)
        self.client_input_box.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        self.client_send_button = Button(self.client_frame, text="Send", command=self.send_message)
        self.client_send_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

        # Create the disconnect button
        self.client_disconnect_button = Button(self.client_frame, text="Disconnect", command=self.disconnect)
        self.client_disconnect_button.grid(row=1, column=1, padx=5, pady=5, sticky="e")

        # Pack the client frame and start the mainloop
        self.client_frame.pack(fill=BOTH, expand=YES)
        self.root.mainloop()
