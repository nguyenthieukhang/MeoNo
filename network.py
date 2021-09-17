import socket
import struct

# A network object whose job is to send and receive integer to the server
class Network:
    def __init__(self, server):
        self.server = server

    def send(self, number: int):
        try:
            #print('Seding netwrok.py line 11', number, type(number))
            packet = struct.pack('!i', int(number))
            self.server.send(packet)
        except Exception as e:
            print('line 15 network.py', str(e))

    def receive(self) -> int :
        try:
            buf = b''
            while len(buf) < 4:
                buf += self.server.recv(8)
            ret = struct.unpack('!i', buf[:4])[0]
            return ret
        except Exception as e:
            print('line 23 network.py', str(e))