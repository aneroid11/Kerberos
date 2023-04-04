import json
import sys
from time import time
import common
from udp_web_node import UDPWebNode
from des import Des


tgs_secret_key = common.gen_key()  # distributed between AuthServer and TicketGrantingServer


class AuthServer(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._login_str = None

        self._sock.bind(('', common.AUTH_SERVER_PORT))

        self._clients = {
            "Anton": common.sha256hash("123"),
            "Maxim": common.sha256hash("1234"),
            "Alexander": common.sha256hash("12345")
        }

    def receive_client_login(self):
        login, addr = self._sock.recvfrom(common.MAX_DATA_LEN)
        login_str = login.decode("utf-8")
        self._login_str = login_str
        print(f"AS: received client login: {login_str}")

        if login_str not in self._clients.keys():
            print("AS: ERROR: no client with such login")
            sys.exit(1)

    def send_ticket_granting_ticket(self):
        tgs_session_key = common.gen_key()

        # TGT
        first_message = {
            "name": self._login_str,
            "tgs_name": "TicketGrantingServer",
            "timestamp": time(),
            "lifetime": 3600.0,
            "tgs_session_key": common.bytes_to_string(tgs_session_key)
        }
        first_message_str = json.dumps(first_message)
        tgs_secret_key_encryptor = Des(bytearray(tgs_secret_key))
        first_message_str_encr = tgs_secret_key_encryptor.encrypt(bytearray(first_message_str, "utf-8"))
        self._send_bytes(first_message_str_encr, common.CLIENT_PORT)

        second_message = {
            "tgs_name": "TicketGrantingServer",
            "tgs_session_key": common.bytes_to_string(tgs_session_key)
        }
        second_message_str = json.dumps(second_message)
        client_secret_key_encryptor = Des(bytearray(self._clients[self._login_str][0:8]))
        self._send_bytes(
            client_secret_key_encryptor.encrypt(bytearray(second_message_str, "utf-8")),
            common.CLIENT_PORT
        )


class TicketGrantingServer(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.TICKET_GRANTING_SERVER_PORT))

        self._services = (
            "ServerService",
            "ServerService1"
        )

    def recv_auth_and_tgt(self):
        data, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        data_dict = json.loads(data.decode("utf-8"))
        # print(data_dict)
        requested_service = data_dict["service_id"]

        if requested_service not in self._services:
            print(f"TGT: No such service: {requested_service}!")
            exit(1)

        tgt_encrypted = common.string_to_bytes(data_dict["ticket_granting_ticket"])
        encryptor = Des(bytearray(tgs_secret_key))
        tgt_decrypted = encryptor.encrypt(bytearray(tgt_encrypted), True).decode("utf-8")
        print(tgt_decrypted)
