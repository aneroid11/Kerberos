from des import Des


def main():
    key = bytearray(0x133457799BBCDFF1.to_bytes(8, "big"))  # BIG
    encryptor = Des(key)

    msg = bytearray("passwordimportant", "utf-8")
    msg_encrypted = encryptor.encrypt(msg)
    print(msg_encrypted)
    msg_decrypted = encryptor.encrypt(msg_encrypted, True)
    print(msg_decrypted)


if __name__ == '__main__':
    main()
