import socket


class ServerService:
    MAX_DATA_LEN = 1024

    def __init__(self):
        self._sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self._sock.bind(('', 50000))

        print("UDP server up and listening")

    def __del__(self):
        self._sock.close()

    def receive_data(self):
        # blocking call
        message, addr = self._sock.recvfrom(ServerService.MAX_DATA_LEN)
        print(f"message {message} from {addr}")
