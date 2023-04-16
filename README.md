# Bluetooth Chat for Raspberry Pi
This program allows two Raspberry Pis to communicate with each other over Bluetooth. The program can run in either server or client mode, depending on the user's choice.

## Requirements
1. Raspberry Pi with Bluetooth capability
2. Python 3
3. PyBluez library installed on both Raspberry Pis. You can install it by running `pip3 install pybluez`.

## Usage
### Command Line
1. Save the chat.py program on both Raspberry Pis.

2. Run the program on the first Raspberry Pi by typing `python3 chat.py` in the terminal.

3. When prompted, enter `1` to start the program in server mode. The program will start listening for a connection from the second Raspberry Pi.

4. Run the program on the second Raspberry Pi by typing `python3 chat.py` in the terminal.

5. When prompted, enter `2` to start the program in client mode. The program will prompt you for the MAC address of the first Raspberry Pi. Enter the MAC address and the two Pis will connect.

6. Once the two Pis are connected, you can start sending messages back and forth by typing them into the terminal on either Pi.

7. To stop the program, use `Ctrl+C` to interrupt the message loop and close the Bluetooth socket.

## Credits
This program was created by Corbin Helms.
