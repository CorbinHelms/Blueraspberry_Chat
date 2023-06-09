import bluetooth
import sys
import threading

class BluetoothChat:
    def __init__(self):
        self.server_sock = None
        self.client_sock = None
        self.client_info = None

    def start_server(self):
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("", bluetooth.PORT_ANY))
        self.server_sock.listen(1)

        port = self.server_sock.getsockname()[1]

        print("Waiting for connection on RFCOMM channel", port)

        self.client_sock, self.client_info = self.server_sock.accept()
        print("Accepted connection from", self.client_info)

    def start_client(self, server_mac_address):
        port = 1

        self.client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        print("Connecting to", server_mac_address)

        self.client_sock.connect((server_mac_address, port))

    def receive_message(self):
        while True:
            data = self.client_sock.recv(1024)
            if not data:
                break
            print("Received message:", data.decode("utf-8"))

        print("Connection closed")
        self.client_sock.close()

    def send_message(self):
        while True:
            message = input("Enter message to send (or 'q' to quit): ")
            if message == 'q':
                break
            self.client_sock.send(message.encode("utf-8"))

        print("Connection closed")
        self.client_sock.close()

    def close(self):
        if self.client_sock:
            self.client_sock.close()
        if self.server_sock:
            self.server_sock.close()

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

    receive_thread = threading.Thread(target=chat.receive_message)
    receive_thread.start()

    send_thread = threading.Thread(target=chat.send_message)
    send_thread.start()

    receive_thread.join()
    send_thread.join()

    chat.close()
