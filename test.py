import bluetooth
import sys
from termcolor import colored

def print_blue(msg):
    print(colored(msg, "blue"))

def print_light_blue(msg):
    print(colored(msg, "powderblue"))

def run_server():
    print_blue("[INFO] Server started...")
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    port = 1
    server_sock.bind(("", port))
    server_sock.listen(1)
    client_sock, client_info = server_sock.accept()
    print_blue("[INFO] Accepted connection from ", end="")
    print_light_blue(client_info)
    while True:
        try:
            data = client_sock.recv(1024).decode().strip()
            if not data:
                continue
            print_blue("[RECEIVED] ", end="")
            print_light_blue(data)
            msg = input(">> ")
            if not msg:
                continue
            client_sock.send(msg.encode())
        except KeyboardInterrupt:
            break
    client_sock.close()
    server_sock.close()
    print_blue("[INFO] Server stopped.")

def run_client():
    print_blue("[INFO] Client started...")
    server_addr = input("Enter the server Bluetooth MAC address: ")
    port = 1
    client_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    client_sock.connect((server_addr, port))
    while True:
        try:
            msg = input(">> ")
            if not msg:
                continue
            client_sock.send(msg.encode())
            data = client_sock.recv(1024).decode().strip()
            if not data:
                continue
            print_blue("[RECEIVED] ", end="")
            print_light_blue(data)
        except KeyboardInterrupt:
            break
    client_sock.close()
    print_blue("[INFO] Client stopped.")

if __name__ == "__main__":
    print_blue("==== Bluetooth Chat ====")
    option = input("Enter 1 for server, 2 for client: ")
    if option == "1":
        run_server()
    elif option == "2":
        run_client()
    else:
        print_blue("Invalid option. Please try again.")
