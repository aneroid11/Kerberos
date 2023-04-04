import socket
import common
from udp_web_node import UDPWebNode


class AuthServer(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.AUTH_SERVER_PORT))

    def receive_client_login(self):
        login, addr = self._sock.recvfrom(common.MAX_DATA_LEN)
        print("client login: " + str(login))

class TicketGrantingServer(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.TICKET_GRANTING_SERVER_PORT))
