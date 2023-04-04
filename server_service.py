import common
from udp_web_node import UDPWebNode


class ServerService(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.SERVER_SERVICE_PORT))

    def recv_auth_and_service_ticket(self):
        data, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        print(data)
        # print(f"message {message}")
