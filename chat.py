import bluetooth
import sys

class BluetoothChat:
    def __init__(self):
        self.server_socket = None
        self.client_socket = None
        self.socket = None

    def start_server(self):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_socket.bind(("", bluetooth.PORT_ANY))
        self.server_socket.listen(1)

        port = self.server_socket.getsockname()[1]
        uuid = "00001101-0000-1000-8000-00805F9B34FB"

        bluetooth.advertise_service(self.server_socket, "BluetoothChat",
                                    service_id=uuid,
                                    service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                    profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                    )
        self.client_socket, client_info = self.server_socket.accept()
        print("Accepted connection from", client_info)

        self.socket = self.client_socket

    def connect_client(self, server_address):
        port = 1
        uuid = "00001101-0000-1000-8000-00805F9B34FB"

        self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_socket.connect((server_address, port))

        self.socket = self.client_socket
        print("Connected to", server_address)

    def send_message(self, message):
        self.socket.send(message.encode())

    def receive_message(self):
        message = self.socket.recv(1024)
        return message.decode()

    def disconnect(self):
        if self.socket:
            self.socket.close()
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
