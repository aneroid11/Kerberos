import socket


class ServerService:
    MAX_DATA_LEN = 1024

    def __init__(self):
        self._sock = socket.socket()
        self._sock.bind(('', 50000))

        print("listen...")
        self._sock.listen(1)
        print("waiting for accept...")
        self._conn_sock, self._client_addr = self._sock.accept()
        print("connected:", self._client_addr)

    def __del__(self):
        self._sock.close()
        self._conn_sock.close()

    def receive_data(self):
        while True:
            data = self._conn_sock.recv(ServerService.MAX_DATA_LEN)
            if not data:
                break
            self._conn_sock.send(data.upper())
