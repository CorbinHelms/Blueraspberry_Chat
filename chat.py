import bluetooth
import threading
import sys

class BluetoothChat:
    def __init__(self, server_address=None):
        self.server_address = server_address
        self.client_socket = None
        self.server_socket = None
        self.running = False

    def start_as_server(self):
        self.running = True
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_socket.bind(("", bluetooth.PORT_ANY))
        self.server_socket.listen(1)

        port = self.server_socket.getsockname()[1]

        bluetooth.advertise_service(
            self.server_socket,
            "BluetoothChat",
            service_id="",
            service_classes=[bluetooth.SERIAL_PORT_CLASS],
            profiles=[bluetooth.SERIAL_PORT_PROFILE],
            #protocols=[bluetooth.OBEX_UUID]
        )

        print("Waiting for connection on RFCOMM channel", port)
        self.client_socket, client_address = self.server_socket.accept()
        print("Accepted connection from", client_address)

    def start_as_client(self, server_address):
        self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_socket.connect((server_address, bluetooth.PORT_ANY))

    def receive_messages(self, receive_callback):
        while self.running:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    receive_callback(data.decode('utf-8'))
                else:
                    print('No more data from', self.client_socket)
                    break
            except ConnectionResetError:
                print('Disconnected')
                break

    def send_message(self, message):
        try:
            self.client_socket.send(message.encode('utf-8'))
        except AttributeError:
            print('Not connected yet')

    def disconnect(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        if self.client_socket:
            self.client_socket.close()
        print('Disconnected')
