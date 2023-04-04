import socket
import common
import datetime
from udp_web_node import UDPWebNode


class Client(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.CLIENT_PORT))

    def _send_string(self, string: str, port: int):
        self._sock.sendto(str.encode(string, "utf-8"), ("localhost", port))

    def send_msg_to_auth_server(self):
        login = input("Enter your login: ")
        self._send_string(login, common.AUTH_SERVER_PORT)
