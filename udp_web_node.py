import socket


class UDPWebNode:
    def __init__(self):
        self._sock = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    def __del__(self):
        self._sock.close()

    def _send_bytes(self, data: bytes, port: int):
        self._sock.sendto(data, ("localhost", port))

    def _send_string(self, string: str, port: int):
        self._send_bytes(str.encode(string, "utf-8"), port)
