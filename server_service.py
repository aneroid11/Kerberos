import socket
import common
from udp_web_node import UDPWebNode


class ServerService(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.SERVER_SERVICE_PORT))

    def receive_data(self):
        # blocking call
        message, addr = self._sock.recvfrom(common.MAX_DATA_LEN)
        print(f"message {message} from {addr}")
