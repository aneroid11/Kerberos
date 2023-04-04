import socket


class Client:
    MAX_DATA_LEN = 1024

    def __init__(self):
        self._sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        print("client is up!")

    def __del__(self):
        self._sock.close()

    def send_data(self):
        self._sock.sendto(str.encode("hello world", "utf-8"), ("localhost", 50000))
