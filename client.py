import socket
import network

HOST = '127.0.0.1'
PORT = 5564
CLIENT = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    CLIENT.connect((HOST, PORT))
    print('Connected to server!')
except socket.error as e:
    print(str(e))

network = network.Network(CLIENT)