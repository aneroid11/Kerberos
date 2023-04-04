import socket


class Client:
    MAX_DATA_LEN = 1024

    def __init__(self):
        self._sock = socket.socket()
        self._sock.connect(('localhost', 50000))
        print("client connected!")

    def __del__(self):
        self._sock.close()

    def send_data(self):
        self._sock.send("hello world")

        response = self._sock.recv(Client.MAX_DATA_LEN)
        print(response)
