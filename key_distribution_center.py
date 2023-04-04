import socket
import common
from udp_web_node import UDPWebNode


class AuthServer(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.AUTH_SERVER_PORT))


class TicketGrantingServer(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.TICKET_GRANTING_SERVER_PORT))
