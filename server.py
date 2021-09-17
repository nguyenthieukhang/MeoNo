import socket
import threading
import struct

import game
import network

HOST = '127.0.0.1'
PORT = 5575
MAX_NUMBER_PLAYER = 1

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen(MAX_NUMBER_PLAYER)
print("The server is listening...")

clients = []

def waiting_for_connection():
    while True:
        print('Waiting for new connection...')
        client, addr = SERVER.accept()
        print('Client', str(addr), 'connected!')
        clients.append(network.Network(client))
        if len(clients) == MAX_NUMBER_PLAYER:
            break

waiting_for_connection()

game_manager = game.Game(clients)
print('Game started')
game_manager.start()