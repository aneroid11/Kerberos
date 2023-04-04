import socket
import common
from udp_web_node import UDPWebNode


class Client(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.CLIENT_PORT))

    def send_data(self):
        self._sock.sendto(str.encode("hello world", "utf-8"), ("localhost", common.SERVER_SERVICE_PORT))
