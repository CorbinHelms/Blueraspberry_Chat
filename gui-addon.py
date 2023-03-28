import tkinter as tk
import threading
from chat import BluetoothChat

class BluetoothChatGUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.server_button = tk.Button(self, text="Start as server", command=self.start_server)
        self.server_button.pack(side="left")

        self.client_frame = tk.Frame(self)
        self.client_label = tk.Label(self.client_frame, text="Server MAC address:")
        self.client_label.pack(side="left")
        self.client_entry = tk.Entry(self.client_frame)
        self.client_entry.pack(side="left")
        self.client_button = tk.Button(self.client_frame, text="Start as client", command=self.start_client)
        self.client_button.pack(side="left")
        self.client_frame.pack(side="left")

        self.receive_text = tk.Text(self, height=10, width=50)
        self.receive_text.pack()
        self.send_frame = tk.Frame(self)
        self.send_label = tk.Label(self.send_frame, text="Enter message:")
        self.send_label.pack(side="left")
        self.send_entry = tk.Entry(self.send_frame)
        self.send_entry.pack(side="left")
        self.send_button = tk.Button(self.send_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="left")
        self.send_frame.pack()

        self.close_button = tk.Button(self, text="Close", command=self.close)
        self.close_button.pack(side="bottom")

    def start_server(self):
        self.chat = BluetoothChat()
        self.chat.start_server()
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.start()

    def start_client(self):
        server_mac_address = self.client_entry.get()
        self.chat = BluetoothChat()
        self.chat.start_client(server_mac_address)
        self.receive_thread = threading.Thread(target=self.receive_message)
        self.receive_thread.start()

    def receive_message(self):
        while True:
            data = self.chat.client_sock.recv(1024)
            if not data:
                break
            self.receive_text.insert(tk.END, data.decode("utf-8"))

        self.receive_text.insert(tk.END, "Connection closed")

    def send_message(self):
        message = self.send_entry.get()
        self.chat.client_sock.send(message.encode("utf-8"))
        self.send_entry.delete(0, tk.END)

    def close(self):
        self.chat.close()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothChatGUI(master=root)
    app.mainloop()
