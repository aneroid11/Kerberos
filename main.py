from des import Des
from client import Client
from key_distribution_center import AuthServer, TicketGrantingServer
from server_service import ServerService

import random


def main():
    random.seed()
    # key = bytearray(0x133457799BBCDFF1.to_bytes(8, "big"))  # BIG
    # encryptor = Des(key)
    #
    # msg = bytearray("passwordimportant", "utf-8")
    # msg_encrypted = encryptor.encrypt(msg)
    # print(msg_encrypted)
    # msg_decrypted = encryptor.encrypt(msg_encrypted, True)
    # print(msg_decrypted)

    client = Client()
    auth_server = AuthServer()
    ticket_granting_server = TicketGrantingServer()

    client.send_msg_to_auth_server()
    auth_server.receive_client_login()

    auth_server.send_ticket_granting_ticket()
    client.receive_ticket_granting_ticket()

    client.send_auth_and_tgt_to_tgs()
    ticket_granting_server.recv_auth_and_tgt()


if __name__ == '__main__':
    main()
