import tkinter as tk
import threading
from chat import BluetoothChat

class BluetoothChatGUI:
    def __init__(self, master):
        self.master = master
        self.master.geometry("640x480")
        self.master.title("Bluetooth Chat")
        self.master.resizable(0, 0)
        self.master.configure(bg="#FFFFFF")
        self.create_widgets()

    def create_widgets(self):
        self.server_button = tk.Button(self.master, text="Start as server", bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12), width=16, height=1, command=self.start_server)
        self.server_button.place(x=20, y=20)

        self.client_label = tk.Label(self.master, text="Server MAC address:", font=("Helvetica", 12), bg="#FFFFFF")
        self.client_label.place(x=150, y=25)
        self.client_entry = tk.Entry(self.master, width=16, font=("Helvetica", 12))
        self.client_entry.place(x=290, y=25)
        self.client_button = tk.Button(self.master, text="Start as client", bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12), width=16, height=1, command=self.start_client)
        self.client_button.place(x=440, y=20)

        self.receive_text = tk.Text(self.master, width=71, height=17, font=("Helvetica", 12))
        self.receive_text.place(x=20, y=70)

        self.send_entry = tk.Entry(self.master, width=49, font=("Helvetica", 12))
        self.send_entry.place(x=20, y=385)
        self.send_button = tk.Button(self.master, text="Send", bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12), width=10, height=1, command=self.send_message)
        self.send_button.place(x=520, y=380)

        self.close_button = tk.Button(self.master, text="Close", bg="#F44336", fg="#FFFFFF", font=("Helvetica", 12), width=10, height=1, command=self.close)
        self.close_button.place(x=520, y=420)

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
    app = BluetoothChatGUI(root)
    root.mainloop()
