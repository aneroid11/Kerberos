from des import Des


def main():
    encryptor = Des()
    print(encryptor.encrypt("55"))
    # print(encryptor.decrypt(encryptor.encrypt("55")))


if __name__ == '__main__':
    main()
