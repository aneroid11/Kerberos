from des import Des


def main():
    key = 0x133457799BBCDFF1
    encryptor = Des(bytearray(key.to_bytes(8, "big")))  # BIG, not little
    # print("\nRESULT")
    msg = 0x0123456789ABCDEF
    # print(encryptor.encrypt("55"))
    print(encryptor.encrypt(bytearray(msg.to_bytes(8, "big"))))
    # print(encryptor.decrypt(encryptor.encrypt("55")))
    print(encryptor.num_to_bitlist(9))


if __name__ == '__main__':
    main()
