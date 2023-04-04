import socket


class UDPWebNode:
    def __init__(self):
        self._sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __del__(self):
        self._sock.close()
