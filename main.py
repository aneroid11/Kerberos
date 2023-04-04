from des import Des


def main():
    key = 0x133457799BBCDFF1
    encryptor = Des(bytearray(key.to_bytes(8, "big")))  # BIG, not little
    # msg = 0x0123456789ABCDEF
    msg = 0x85e813540f0ab405  # encrypted version

    msg_encrypted = encryptor.encrypt(bytearray(msg.to_bytes(8, "big")), True)
    msg_encr_num = int.from_bytes(msg_encrypted, "big")
    print(hex(msg_encr_num))


if __name__ == '__main__':
    main()
