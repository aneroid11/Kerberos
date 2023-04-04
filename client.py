import time

import common
import sys
import json
from udp_web_node import UDPWebNode
from des import Des


class Client(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._tgs_session_key = None
        self._ticket_granting_ticket = None
        self._sock.bind(('', common.CLIENT_PORT))

        self._login = None

    def send_msg_to_auth_server(self):
        self._login = input("Enter your login: ")
        print("sending login to AS...")
        self._send_string(self._login, common.AUTH_SERVER_PORT)

    def receive_ticket_granting_ticket(self):
        self._ticket_granting_ticket, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        second_message, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        password = input("Enter your password: ")
        client_secret_key = bytearray(common.sha256hash(password)[0:8])
        encryptor = Des(client_secret_key)
        second_msg_decr = common.delete_trailing_zeros(encryptor.encrypt(bytearray(second_message), True))

        try:
            second_data_str = second_msg_decr.decode("utf-8")
            second_data = json.loads(second_data_str)
        except Exception as e:
            print("Password is incorrect!")
            sys.exit(1)

        print(second_data)
        self._tgs_session_key = common.string_to_bytes(second_data["tgs_session_key"])

    def send_auth_and_tgt_to_tgs(self):
        auth1 = {
            "client_id": self._login,
            "timestamp": time.time()
        }
        encryptor = Des(bytearray(self._tgs_session_key))
        auth1_encrypted = encryptor.encrypt(bytearray(json.dumps(auth1).encode("utf-8")))

        data = {
            "service_id": "ServerService",
            "ticket_granting_ticket": common.bytes_to_string(self._ticket_granting_ticket),
            "auth1": common.bytes_to_string(auth1_encrypted)
        }

        self._send_string(json.dumps(data), common.TICKET_GRANTING_SERVER_PORT)

    def recv_service_ticket_and_session_key(self):
        service_ticket_encrypted, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        msg2_encrypted, _ = self._sock.recvfrom(common.MAX_DATA_LEN)

        encryptor = Des(bytearray(self._tgs_session_key))
        msg2_decrypted = common.delete_trailing_zeros(encryptor.encrypt(
            bytearray(msg2_encrypted),
            True
        )).decode("utf-8")
        msg2_dict = json.loads(msg2_decrypted)
        print(msg2_dict)
