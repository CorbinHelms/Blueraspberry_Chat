import subprocess
import tkinter as tk

class BluetoothChatGUI:
    def __init__(self, master):
        self.master = master

        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.text_box = tk.Text(self.frame, width=50, height=20)
        self.text_box.pack()

        self.entry_label = tk.Label(self.frame, text="Enter message:")
        self.entry_label.pack()

        self.entry_box = tk.Entry(self.frame)
        self.entry_box.pack()

        self.send_button = tk.Button(self.frame, text="Send", command=self.send_message)
        self.send_button.pack()

        self.receive_messages()

    def receive_messages(self):
        while True:
            message = self.master.receive_message()
            if message:
                self.text_box.insert(tk.END, message + "\n")

    def send_message(self):
        message = self.entry_box.get()
        self.entry_box.delete(0, tk.END)
        self.master.send_message(message)

if __name__ == "__main__":
    chat_process = subprocess.Popen(["python3", "chat.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    root = tk.Tk()
    root.title("Bluetooth Chat")

    gui = BluetoothChatGUI(chat_process)

    root.mainloop()
