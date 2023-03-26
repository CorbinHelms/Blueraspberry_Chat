import bluetooth

def start_server():
    # Set up the Bluetooth socket
    server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1  # This can be any free port
    server_socket.bind(("", port))
    server_socket.listen(1)  # Listen for one incoming connection

    # Wait for a client to connect
    print("Waiting for connection...")
    client_socket, address = server_socket.accept()
    print("Accepted connection from", address)

    # Start the message loop
    while True:
        # Wait for input from the user
        message = input("Type your message: ")

        # Send the message to the client
        client_socket.send(message.encode())

        # Receive the client's response
        data = client_socket.recv(1024)
        print("Received:", data.decode())

def start_client():
    # Set up the Bluetooth socket
    client_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    # Get the server's MAC address
    server_address = input("Enter the server's MAC address: ")
    port = 1  # This should match the port used by the server
    client_socket.connect((server_address, port))

    # Start the message loop
    while True:
        # Wait for input from the user
        message = input("Type your message: ")

        # Send the message to the server
        client_socket.send(message.encode())

        # Receive the server's response
        data = client_socket.recv(1024)
        print("Received:", data.decode())

# Ask the user which mode to start in
while True:
    mode = input("Enter 1 for server or 2 for client: ")
    if mode == "1":
        start_server()
        break
    elif mode == "2":
        start_client()
        break
    else:
        print("Invalid option. Please enter 1 for server or 2 for client.")
