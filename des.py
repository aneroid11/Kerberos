# from bitarray import bitarray


class Des:
    def _correct_pc_1(self):
        for i in range(len(self._pc_1)):
            self._pc_1[i] -= 1

    def __init__(self, plain_message: str, key: bytearray):
        self._pc_1 = [
            57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4
        ]
        self._correct_pc_1()

        self._plain_data = bytearray(plain_message, "utf-8")
        self._key = key
        self._key_bits = []
        self._key_bits_56 = []

        self._key_to_key_bits()
        self._key_initial_permutation()
        self._key_c = [self._key_bits_56[0:28]]
        self._key_d = [self._key_bits_56[28:56]]
        print(self._key_c[0])
        print(self._key_d[0])

        self._create_key_cds()
        print(self._key_c[0:17])
        print(self._key_d[0:17])

        self._encrypted_data = bytearray()

    def _access_bit(self, data: bytearray, num: int):
        base = int(num // 8)
        shift = int(num % 8)

        # return (data[base] << shift) & 0x80
        return (((data[base] << shift) % 256) & 0x80) >> 7

    def _key_to_key_bits(self):
        for i in range(64):
            bit = self._access_bit(self._key, i)
            self._key_bits.append(bit)
            print(bit, end="")
        print()

    def _key_initial_permutation(self):
        for i in range(56):
            self._key_bits_56.append(self._key_bits[self._pc_1[i]])

    def _cycle_lshift_bitarray(self, arr: list, num: int) -> list:
        return arr[num:] + arr[:num]

    def _create_key_cds(self):
        left_shifts = (1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1)

        for i in range(1, 17):
            self._key_c.append(self._cycle_lshift_bitarray(self._key_c[i - 1], left_shifts[i - 1]))
            self._key_d.append(self._cycle_lshift_bitarray(self._key_d[i - 1], left_shifts[i - 1]))

    def _append_zeros_to_plain_data(self):
        plain_data_len = len(self._plain_data)
        zeros_to_add = 8 - plain_data_len % 8

        if zeros_to_add == 8:
            return

        for _ in range(zeros_to_add):
            self._plain_data.append(0)

    def _encrypt_block(self, curr_block: bytearray) -> bytearray:
        left = curr_block[0:4]
        right = curr_block[4:8]
        return curr_block

    def encrypt(self) -> str:
        self._append_zeros_to_plain_data()

        # now we need to cipher it block by block (block size == 64 bit == 8 bytes)
        num_on_blocks = int(len(self._plain_data) / 8)
        for i in range(num_on_blocks):
            block_start = i * 8
            block_end = block_start + 8
            curr_block = self._plain_data[block_start:block_end]
            self._encrypted_data += self._encrypt_block(curr_block)

        return str(self._encrypted_data)

    # def decrypt(self, encr_msg: str) -> str:
    # return encr_msg