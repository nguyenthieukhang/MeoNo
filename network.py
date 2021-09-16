import socket
import struct

# A network object whose job is to send and receive integer to the server
class Network:
    def __init__(self, server):
        self.server = server

    def send(self, number: int):
        try:
            packet = struct.pack('i', number)
            self.server.send(packet)
        except Exception as e:
            print(str(e))

    def receive(self) -> int :
        try:
            signal = self.server.recv(4)
            ret = struct.unpack('i', signal)[0]
            return ret
        except Exception as e:
            print(str(e))