import socket
import common
import datetime
from udp_web_node import UDPWebNode


class Client(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.CLIENT_PORT))

    def send_msg_to_auth_server(self):
        login = input("Enter your login: ")
        print("sending login to AS...")
        self._send_string(login, common.AUTH_SERVER_PORT)

    def receive_ticket_granting_ticket(self):
        pass
