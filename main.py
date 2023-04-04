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
    server_service = ServerService()

    client.send_msg_to_auth_server()
    auth_server.receive_client_login()

    auth_server.send_ticket_granting_ticket()
    client.receive_ticket_granting_ticket()

    client.send_auth_and_tgt_to_tgs()
    ticket_granting_server.recv_auth_and_tgt()

    ticket_granting_server.send_service_ticket_and_session_key_to_client()
    client.recv_service_ticket_and_session_key()

    client.send_auth_and_service_ticket_to_service()
    server_service.recv_auth_and_service_ticket()


if __name__ == '__main__':
    main()
