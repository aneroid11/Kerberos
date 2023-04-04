import common
import sys
import json
from udp_web_node import UDPWebNode
from des import Des


class Client(UDPWebNode):
    def __init__(self):
        super().__init__()
        self._sock.bind(('', common.CLIENT_PORT))

    def send_msg_to_auth_server(self):
        login = input("Enter your login: ")
        print("sending login to AS...")
        self._send_string(login, common.AUTH_SERVER_PORT)

    def receive_ticket_granting_ticket(self):
        # data, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        # key = 0x133457799BBCDFF1.to_bytes(8, "big")
        # encryptor = Des(bytearray(key))
        # data_decrypted = encryptor.encrypt(bytearray(data), True).decode("utf-8")
        # print(data_decrypted)
        first_message, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        second_message, _ = self._sock.recvfrom(common.MAX_DATA_LEN)
        password = input("Enter your password: ")
        client_secret_key = bytearray(common.sha256hash(password)[0:8])
        encryptor = Des(client_secret_key)
        second_msg_decr = encryptor.encrypt(bytearray(second_message), True)
        print(second_msg_decr)

        print(json.loads('{"tgs_name": "TicketGrantingServer", "tgs_session_key": "YotoXjUgMpI="}'))

        try:
            # second_data = json.loads(second_msg_decr.decode("utf-8"))
            second_data_str = second_msg_decr.decode("utf-8")
            print(second_data_str)
            second_data = json.loads(second_data_str)
        except Exception as e:
            print("Password is incorrect!")
            print(e)
            sys.exit(1)

        print(second_data)
