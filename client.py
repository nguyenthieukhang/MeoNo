import socket

import constants
import network
import playermanager

HOST = '127.0.0.1'
PORT = 5590
SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    SERVER.connect((HOST, PORT))
    print('Connected to server!')
except socket.error as e:
    print(str(e))

player_manager = playermanager.PlayerManager(SERVER)
player_manager.start()

SERVER.close()







