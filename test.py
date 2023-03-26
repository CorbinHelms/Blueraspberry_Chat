import tkinter as tk
import threading
import subprocess


class ChatGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Chat Program")
        self.window.geometry("400x200")
        
        # Create start buttons
        self.server_button = tk.Button(self.window, text="Start as Server", command=self.start_server)
        self.client_button = tk.Button(self.window, text="Start as Client", command=self.start_client)
        self.server_button.pack(side=tk.LEFT, padx=10, pady=10)
        self.client_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        self.window.mainloop()

    def start_server(self):
        # Create server window
        self.server_window = tk.Toplevel(self.window)
        self.server_window.title("Server Window")
        self.server_window.geometry("400x200")
        
        # Create waiting label
        self.waiting_label = tk.Label(self.server_window, text="Waiting for client...")
        self.waiting_label.pack(padx=10, pady=10)
        
        # Start server in a separate thread
        threading.Thread(target=subprocess.run, args=(["python", "chat.py", "-s"],)).start()
        
        # Disable server button to prevent starting multiple servers
        self.server_button.config(state=tk.DISABLED)
        
    def start_client(self):
        # Create client window
        self.client_window = tk.Toplevel(self.window)
        self.client_window.title("Client Window")
        self.client_window.geometry("400x200")
        
        # Create MAC address entry and connect button
        self.mac_label = tk.Label(self.client_window, text="Enter Server MAC Address:")
        self.mac_label.pack(padx=10, pady=10)
        self.mac_entry = tk.Entry(self.client_window)
        self.mac_entry.pack(padx=10, pady=10)
        self.connect_button = tk.Button(self.client_window, text="Connect", command=self.connect_to_server)
        self.connect_button.pack(padx=10, pady=10)
        
        # Disable client button to prevent starting multiple clients
        self.client_button.config(state=tk.DISABLED)

    def connect_to_server(self):
        # Get MAC address from entry box
        mac_address = self.mac_entry.get()
        
        # Start client in a separate thread
        threading.Thread(target=subprocess.run, args=(["python", "chat.py", "-c", mac_address],)).start()
        
        # Destroy client window
        self.client_window.destroy()
        
        # Create chat window
        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.title("Chat Window")
        self.chat_window.geometry("400x200")
        
        # Create chat box, message entry and send button
        self.chat_box = tk.Text(self.chat_window)
        self.chat_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.message_entry = tk.Entry(self.chat_window)
        self.message_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.send_button = tk.Button(self.chat_window, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Create disconnect button
        self.disconnect_button = tk.Button(self.chat_window, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Disable message entry, send button, and disconnect button until connected
        self.message_entry.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.disconnect_button.config(state=tk.DISABLED)
        self.send_button = Button(self.chat_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=RIGHT, padx=5)
        
        self.disconnect_button = Button(self.chat_frame, text="Disconnect", command=self.disconnect)
        self.disconnect_button.pack(side=RIGHT, padx=5)
        
        self.message_box = Text(self.chat_frame, state=DISABLED)
        self.message_box.pack(side=BOTTOM, fill=BOTH, expand=True)
        
        # Start the GUI
        self.root.mainloop()
        
if __name__ == '__main__':
    ChatGUI()

