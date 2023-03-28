import bluetooth
import sys
import threading

class BluetoothChat:
    def __init__(self, server_address=None):
        self.server_address = server_address
        self.client_socket = None
        self.server_socket = None
        self.running = False
        
    def start_server(self):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_socket.bind(("", bluetooth.PORT_ANY))
        self.server_socket.listen(1)

        port = self.server_socket.getsockname()[1]

        uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

        bluetooth.advertise_service(self.server_socket, "BluetoothChat",
                                    service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE])

        print("Waiting for connection on RFCOMM channel", port)

        self.client_socket, client_address = self.server_socket.accept()
        print("Accepted connection from", client_address)

        self.running = True
        
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print("Received", data.decode())
            except OSError:
                break

    def connect_client(self, server_address):
        self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_socket.connect((server_address, bluetooth.PORT_ANY))

        print("Connected to", server_address)

        self.running = True
        
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                print("Received", data.decode())
            except OSError:
                break

    def send_message(self, message):
        if self.client_socket:
            self.client_socket.send(message.encode())
        elif self.server_socket:
            self.client_socket.send(message.encode())

    def disconnect(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
        elif self.server_socket:
            self.server_socket.close()

class BluetoothChatThread(threading.Thread):
    def __init__(self, chat):
        threading.Thread.__init__(self)
        self.chat = chat
        
    def run(self):
        if self.chat.server_address:
            self.chat.start_server()
        else:
            self.chat.connect_client()

if __name__ == '__main__':
    chat = BluetoothChat()
    chat_thread = BluetoothChatThread(chat)
    chat_thread.start()

    while True:
        message = input("Enter message: ")
        chat.send_message(message)

        if message == 'quit':
            chat.disconnect()
            sys.exit(0)
