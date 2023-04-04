import common
import json
import time
from udp_web_node import UDPWebNode
from des import Des


class ServerService(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._service_session_key = None
        self._auth2_timestamp = None
        self._service_secret_key = None
        self._sock.bind(('', common.SERVER_SERVICE_PORT))

    def recv_service_secret_key(self):
        self._service_secret_key, _ = self._sock.recvfrom(common.MAX_DATA_LEN)

    def recv_auth_and_service_ticket(self):
        data, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        data_dict = json.loads(data.decode("utf-8"))
        ticket_encrypted = common.string_to_bytes(data_dict["service_ticket"])
        auth2_encrypted = common.string_to_bytes(data_dict["auth2"])

        encryptor = Des(bytearray(self._service_secret_key))
        ticket_decrypted = common.delete_trailing_zeros(encryptor.encrypt(bytearray(ticket_encrypted), True))\
            .decode("utf-8")
        ticket_dict = json.loads(ticket_decrypted)
        print(ticket_dict)

        self._service_session_key = common.string_to_bytes(ticket_dict["service_session_key"])
        encryptor = Des(bytearray(self._service_session_key))
        auth2_decrypted = common.delete_trailing_zeros(encryptor.encrypt(bytearray(auth2_encrypted),
                                                                         True)).decode("utf-8")
        auth2_dict = json.loads(auth2_decrypted)
        print(auth2_dict)

        if auth2_dict["client_id"] != ticket_dict["client_id"]:
            print("SS: Client ids from auth2 and TGS do not match!")
            exit(1)
        if auth2_dict["timestamp"] - ticket_dict["timestamp"] > 120.0:
            print("SS: The timestamps of auth2 and TGS differ by more than two minutes!")
            exit(1)
        if ticket_dict["timestamp"] + ticket_dict["lifetime"] < time.time():
            print("SS: The TGS has expired!")
            exit(1)

        self._auth2_timestamp = auth2_dict["timestamp"]
        print(f"SS: CLIENT {auth2_dict['client_id']} AUTHENTICATED")

    def send_modificated_time_to_client(self):
        encryptor = Des(bytearray(self._service_session_key))
        timestamp_encrypted = encryptor.encrypt(
            bytearray(str(self._auth2_timestamp + 1).encode("utf-8"))
        )
        self._send_bytes(timestamp_encrypted, common.CLIENT_PORT)
