from des import Des
from client import Client
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
    server_service = ServerService()
    client = Client()

    client.send_data()
    server_service.receive_data()


if __name__ == '__main__':
    main()
