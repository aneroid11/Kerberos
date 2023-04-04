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
        print("AS: Send TGT and TGS session key")

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
        self._tgs_session_key = None
        self._service_secret_key = common.gen_key()
        self._requested_service = None
        self._client_id = None
        self._sock.bind(('', common.TICKET_GRANTING_SERVER_PORT))

        self._services = (
            "ServerService",
            "ServerService1"
        )

    def send_service_secret_key_to_server_service(self):
        self._send_bytes(self._service_secret_key, common.SERVER_SERVICE_PORT)

    def recv_auth_and_tgt(self):
        print("TGS: Receive auth1 and TGT")

        data, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        data_dict = json.loads(data.decode("utf-8"))
        self._requested_service = data_dict["service_id"]

        if self._requested_service not in self._services:
            print(f"TGS: No such service: {self._requested_service}!")
            exit(1)

        tgt_encrypted = common.string_to_bytes(data_dict["ticket_granting_ticket"])
        encryptor = Des(bytearray(tgs_secret_key))
        tgt_decrypted = common.delete_trailing_zeros(encryptor.encrypt(bytearray(tgt_encrypted), True)).decode("utf-8")
        tgt_decrypted_dict = json.loads(tgt_decrypted)

        self._tgs_session_key = common.string_to_bytes(tgt_decrypted_dict["tgs_session_key"])
        # decrypt auth1
        auth1 = common.string_to_bytes(data_dict["auth1"])
        encryptor = Des(bytearray(self._tgs_session_key))
        auth1_decrypted = common.delete_trailing_zeros(encryptor.encrypt(bytearray(auth1), True)).decode("utf-8")
        auth1_decrypted_dict = json.loads(auth1_decrypted)

        self._client_id = auth1_decrypted_dict["client_id"]

        if tgt_decrypted_dict["name"] != auth1_decrypted_dict["client_id"]:
            print("TGS: Client names in TGT and auth1 do not match!")
            exit(1)
        if auth1_decrypted_dict["timestamp"] - tgt_decrypted_dict["timestamp"] > 120.0:
            print("TGS: The timestamps of auth1 and TGT differ by more than two minutes!")
            exit(1)
        if tgt_decrypted_dict["timestamp"] + tgt_decrypted_dict["lifetime"] < time():
            print("TGS: The TGT has expired!")
            exit(1)

    def send_service_ticket_and_session_key_to_client(self):
        print("TGS: Send service ticket and session key to client")

        service_session_key = common.gen_key()
        timestamp = time()

        service_ticket = {
            "client_id": self._client_id,
            "service_id": self._requested_service,
            "timestamp": timestamp,
            "lifetime": 900.0,
            "service_session_key": common.bytes_to_string(service_session_key)
        }
        msg2 = {
            "service_id": self._requested_service,
            "timestamp": timestamp,
            "lifetime": 900.0,
            "service_session_key": common.bytes_to_string(service_session_key)
        }
        encryptor = Des(bytearray(self._service_secret_key))
        service_ticket_encrypted = encryptor.encrypt(bytearray(json.dumps(service_ticket), "utf-8"))
        self._send_bytes(service_ticket_encrypted, common.CLIENT_PORT)

        encryptor = Des(bytearray(self._tgs_session_key))
        msg2_encrypted = encryptor.encrypt(bytearray(json.dumps(msg2), "utf-8"))
        self._send_bytes(msg2_encrypted, common.CLIENT_PORT)
