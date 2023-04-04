from des import Des
from client import Client
from key_distribution_center import AuthServer, TicketGrantingServer
from server_service import ServerService


def main():
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

    client.send_msg_to_auth_server()
    auth_server.receive_client_login()

if __name__ == '__main__':
    main()
