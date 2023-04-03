from des import Des


def main():
    key = 0x133457799BBCDFF1
    encryptor = Des("55", bytearray(key.to_bytes(8, "big")))  # BIG, not little
    print("\nRESULT")
    print(encryptor.encrypt())
    # print(encryptor.decrypt(encryptor.encrypt("55")))


if __name__ == '__main__':
    main()
