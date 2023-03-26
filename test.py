import tkinter as tk
import threading
import queue
from chat import BluetoothChat

class ChatGUI:
    def __init__(self, chat):
        self.chat = chat
        self.root = tk.Tk()
        self.root.title("Bluetooth Chat")
        self.message_queue = queue.Queue()
        self.setup_ui()

    def setup_ui(self):
        # Create GUI elements
        self.message_list = tk.Listbox(self.root, width=50, height=20)
        self.message_list.pack(side=tk.LEFT, padx=10, pady=10)

        self.send_frame = tk.Frame(self.root)
        self.send_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.send_label = tk.Label(self.send_frame, text="Enter message:")
        self.send_label.pack(side=tk.TOP, pady=5)

        self.send_entry = tk.Entry(self.send_frame, width=30)
        self.send_entry.pack(side=tk.TOP, pady=5)

        self.send_button = tk.Button(self.send_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.TOP, pady=5)

        # Start threads for receiving and displaying messages
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

        display_thread = threading.Thread(target=self.display_messages)
        display_thread.start()

    def receive_message(self):
        while True:
            data = self.chat.client_sock.recv(1024)
            if not data:
                break
            self.message_queue.put(data.decode("utf-8"))

        self.message_queue.put("Connection closed")
        self.chat.client_sock.close()

    def send_message(self):
        message = self.send_entry.get()
        if message:
            self.chat.client_sock.send(message.encode("utf-8"))
            self.send_entry.delete(0, tk.END)

    def display_messages(self):
        while True:
            try:
                message = self.message_queue.get(block=False)
                self.message_list.insert(tk.END, message)
                self.message_list.see(tk.END)
            except queue.Empty:
                pass

            if not self.chat.client_sock or self.chat.client_sock.closed:
                break

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    chat = BluetoothChat()

    mode = input("Enter 1 to start as server, or 2 to start as client: ")
    if mode == "1":
        chat.start_server()
    elif mode == "2":
        server_mac_address = input("Enter server MAC address: ")
        chat.start_client(server_mac_address)
    else:
        print("Invalid option")
        exit()

    gui = ChatGUI(chat)

    gui.run()
