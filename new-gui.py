import tkinter as tk
from tkinter import messagebox
from tkinter import *
import tkinter.font as tkFont
import threading
import time
import bluetooth

class BluetoothChat:

    def __init__(self, server_mac_address):
        self.server_mac_address = server_mac_address
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_socket = None
        self.client_address = None
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.daemon = True
        self.send_thread = threading.Thread(target=self.send_messages)
        self.send_thread.daemon = True

    def start_server(self):
        self.server_socket.bind((self.server_mac_address, 1))
        self.server_socket.listen(1)
        self.client_socket, self.client_address = self.server_socket.accept()
        self.receive_thread.start()
        self.send_thread.start()

    def connect_client(self, server_mac_address):
        port = 1
        self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_socket.connect((server_mac_address, port))
        self.receive_thread.start()
        self.send_thread.start()

    def send_messages(self):
        while True:
            message = input("Enter message to send:")
            self.client_socket.send(message)

    def receive_messages(self):
        while True:
            message = self.client_socket.recv(1024).decode('utf-8')
            print("Received message:", message)

class GUI:

    def __init__(self, master):
        self.master = master
        self.master.geometry("400x300")
        self.master.title("Bluetooth Chat")

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.server_button = tk.Button(self.frame, text="Start Server", command=self.start_server)
        self.server_button.pack(side=tk.LEFT)

        self.client_button = tk.Button(self.frame, text="Connect to Server", command=self.connect_client)
        self.client_button.pack(side=tk.LEFT)

        self.text_area = tk.Text(self.master)
        self.text_area.pack()

    def start_server(self):
        messagebox.showinfo("Information", "Server Started")

    def connect_client(self):
        server_address = tk.simpledialog.askstring("Input", "Enter server MAC address:")
        messagebox.showinfo("Information", "Connecting to " + server_address)
        chat = BluetoothChat(server_address)
        chat.connect_client(server_address)

class ChatWindow(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.grid(sticky=N+S+E+W)
        self.createWidgets()

    def createWidgets(self):
        # create text box for message display
        self.displayBox = Text(self, state=DISABLED, wrap=WORD)
        self.displayBox.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky=N+S+E+W)

        # create label for message entry box
        self.messageLabel = Label(self, text="Enter Message:")
        self.messageLabel.grid(row=1, column=0, padx=5, pady=5, sticky=W)

        # create message entry box
        self.messageBox = Entry(self)
        self.messageBox.grid(row=1, column=1, padx=5, pady=5, sticky=N+S+E+W)

        # create send button
        self.sendButton = Button(self, text="Send", command=self.sendMessage)
        self.sendButton.grid(row=2, column=0, padx=5, pady=5, sticky=W)

        # create quit button
        self.quitButton = Button(self, text="Quit", command=self.quit)
        self.quitButton.grid(row=2, column=1, padx=5, pady=5, sticky=E)

    def sendMessage(self):
        message = self.messageBox.get()
        self.displayMessage("Me: " + message)
        self.messageBox.delete(0, END)
        if bt is not None:
            bt.send(message)

    def displayMessage(self, message):
        self.displayBox.config(state=NORMAL)
        self.displayBox.insert(END, message + "\n")
        self.displayBox.see(END)
        self.displayBox.config(state=DISABLED)

    def run(self):
        """
        The run() method is called when the thread is started. It manages the Bluetooth connection
        and continuously listens for incoming messages from the remote device. Any incoming messages
        are then passed to the GUI thread using the queue.
        """
        self.server_sock=BluetoothSocket( RFCOMM )
        self.server_sock.bind(("",self.port))
        self.server_sock.listen(1)

        self.client_sock,address = self.server_sock.accept()
        print(f"Accepted connection from {address}")

        while True:
            try:
                data = self.client_sock.recv(1024)
                if len(data) == 0: break
                self.queue.put(data.decode())
            except OSError:
                break

        self.client_sock.close()
        self.server_sock.close()
