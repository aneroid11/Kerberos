from des import Des


def main():
    key = bytearray(0x133457799BBCDFF1.to_bytes(8, "big"))  # BIG
    encryptor = Des(key)

    msg = bytearray("passwordimportant", "utf-8")
    msg_encrypted = encryptor.encrypt(msg)
    print(msg_encrypted)
    msg_decrypted = encryptor.encrypt(msg_encrypted, True)
    print(msg_decrypted)

    # msg = 0x0123456789ABCDEF
    # msg = 0x85e813540f0ab405  # encrypted version
    #
    # msg_encrypted = encryptor.encrypt(bytearray(msg.to_bytes(8, "big")), True)
    # msg_encr_num = int.from_bytes(msg_encrypted, "big")
    # print(hex(msg_encr_num))


if __name__ == '__main__':
    main()
