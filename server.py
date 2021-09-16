import socket
import threading
import struct

HOST = '127.0.0.1'
PORT = 5564
MAX_NUMBER_PLAYER = 6

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
SERVER.bind((HOST, PORT))
SERVER.listen(MAX_NUMBER_PLAYER)
print("The server is listening...")

def handle(client):
    print("Handling client", str(client))
    while True:
        try:
            msg = client.recv(4)
            msg = struct.unpack('i', msg)[0]
            reply = struct.pack('i', msg)
            client.send(reply)
        except Exception as e:
            print(str(e))
            break

def main():
    while True:
        print('Waiting for new connection...')
        client, addr = SERVER.accept()
        print('Client', str(addr), 'connected!')
        handle_thread = threading.Thread(target=handle, args=(client, ))
        handle_thread.start()

main()
