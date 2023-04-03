class Des:
    def _correct_pc_1(self):
        for i in range(len(self._pc_1)):
            self._pc_1[i] -= 1

    def __init__(self, key: bytearray):
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

        self._key = key
        self._key_bits = []
        self._key_bits_56 = []

        self._key_to_key_bits()
        self._key_initial_permutation()
        self._key_c = [self._key_bits_56[0:28]]
        self._key_d = [self._key_bits_56[28:56]]

        self._create_key_cds()
        self._keys_48 = []
        self._create_16_keys_from_cds()

    def _access_bit(self, data: bytearray, num: int):
        base = int(num // 8)
        shift = int(num % 8)

        # return (data[base] << shift) & 0x80
        return (((data[base] << shift) % 256) & 0x80) >> 7

    def _key_to_key_bits(self):
        for i in range(64):
            bit = self._access_bit(self._key, i)
            self._key_bits.append(bit)

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

    def _create_16_keys_from_cds(self):
        pc_2 = [
            14, 17, 11, 24, 1, 5,
            3, 28, 15, 6, 21, 10,
            23, 19, 12, 4, 26, 8,
            16, 7, 27, 20, 13, 2,
            41, 52, 31, 37, 47, 55,
            30, 40, 51, 45, 33, 48,
            44, 49, 39, 56, 34, 53,
            46, 42, 50, 36, 29, 32
        ]
        pc_2 = [x - 1 for x in pc_2]

        for i in range(1, 17):
            curr_key = []
            key_before_permutation = self._key_c[i] + self._key_d[i]
            for j in range(48):
                curr_key.append(key_before_permutation[pc_2[j]])

            self._keys_48.append(curr_key)


    def _append_zeros_to_plain_data(self, plain_data: bytearray):
        plain_data_len = len(plain_data)
        zeros_to_add = 8 - plain_data_len % 8

        if zeros_to_add == 8:
            return

        for _ in range(zeros_to_add):
            plain_data.append(0)

    def _msg_initial_permutation(self, curr_block_bits: list) -> list:
        ip = [
            58, 50, 42, 34, 26, 18, 10, 2,
            60, 52, 44, 36, 28, 20, 12, 4,
            62, 54, 46, 38, 30, 22, 14, 6,
            64, 56, 48, 40, 32, 24, 16, 8,
            57, 49, 41, 33, 25, 17, 9, 1,
            59, 51, 43, 35, 27, 19, 11, 3,
            61, 53, 45, 37, 29, 21, 13, 5,
            63, 55, 47, 39, 31, 23, 15, 7
        ]
        ip = [x - 1 for x in ip]

        perm_bits = [curr_block_bits[ip[i]] for i in range(64)]
        return perm_bits


    def _encrypt_block(self, curr_block: bytearray) -> bytearray:
        curr_block_bits = [self._access_bit(curr_block, i) for i in range(64)]
        initial_permutation = self._msg_initial_permutation(curr_block_bits)
        print(initial_permutation)

        return curr_block

    def encrypt(self, plain_data: bytearray) -> bytearray:
        # plain_data = bytearray(plain_message, "utf-8")
        encrypted_data = bytearray()
        self._append_zeros_to_plain_data(plain_data)

        # now we need to cipher it block by block (block size == 64 bit == 8 bytes)
        num_on_blocks = int(len(plain_data) / 8)
        for i in range(num_on_blocks):
            block_start = i * 8
            block_end = block_start + 8
            curr_block = plain_data[block_start:block_end]
            encrypted_data += self._encrypt_block(curr_block)

        print()
        return encrypted_data
