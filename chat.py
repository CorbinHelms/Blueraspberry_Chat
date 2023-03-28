import bluetooth
import threading

class BluetoothChat:
    def __init__(self, server_address=None):
        self.server_address = server_address
        self.client_socket = None
        self.server_socket = None
        self.receive_thread = None
        self.connected = False

    def start_server(self):
        self.server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_socket.bind(("", bluetooth.PORT_ANY))
        self.server_socket.listen(1)
        self.port = self.server_socket.getsockname()[1]
        uuid = "00001101-0000-1000-8000-00805F9B34FB"
        bluetooth.advertise_service(self.server_socket, "BluetoothChat",
                                     service_id=uuid,
                                     service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                     profiles=[bluetooth.SERIAL_PORT_PROFILE])
        print(f"Waiting for connection on RFCOMM channel {self.port}")
        self.client_socket, client_info = self.server_socket.accept()
        print(f"Accepted connection from {client_info}")
        self.connected = True
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def connect_client(self, server_address):
        self.client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.client_socket.connect((server_address, bluetooth.PORT_ANY))
        print(f"Connected to {server_address}")
        self.connected = True
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def receive(self):
        while self.connected:
            try:
                data = self.client_socket.recv(1024)
                if data:
                    print(data.decode("utf-8"))
            except bluetooth.btcommon.BluetoothError:
                self.connected = False
                print("Disconnected")
                self.client_socket.close()

    def send(self, message):
        if self.connected:
            self.client_socket.send(message.encode("utf-8"))

    def disconnect(self):
        self.connected = False
        self.client_socket.close()
        self.server_socket.close()
