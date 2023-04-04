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
        pos_in_byte = int(num % 8)
        shift = 7 - pos_in_byte

        return (data[base] >> shift) & 0x1
        # return (data[base] << shift) & 0x80
        # return (((data[base] << shift) % 256) & 0x80) >> 7

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

    def _calculate_e(self, data: list) -> list:
        selection_table = [
            32, 1, 2, 3, 4, 5,
            4, 5, 6, 7, 8, 9,
            8, 9, 10, 11, 12, 13,
            12, 13, 14, 15, 16, 17,
            16, 17, 18, 19, 20, 21,
            20, 21, 22, 23, 24, 25,
            24, 25, 26, 27, 28, 29,
            28, 29, 30, 31, 32, 1
        ]
        ret = [data[selection_table[i] - 1] for i in range(48)]
        return ret

    def _bitlist_to_num(self, bitlist: list) -> int:
        length = len(bitlist)
        out = 0

        for bit in bitlist:
            out = (out << 1) | bit

        return out

    def _num_to_bitlist(self, num: int, num_bits=None) -> list:
        out = []

        if num_bits is None:
            while num != 0:
                out.insert(0, num & 0x1)
                num = num >> 1
        else:
            for _ in range(num_bits):
                out.insert(0, num & 0x1)
                num = num >> 1
        return out

    def _calculate_s_box(self, index: int, curr_group: list) -> list:
        s_list = [
            [
                [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
                [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
                [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
                [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
            ],
            [
                [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12,0,5,10],
                [3,13,4, 7, 15, 2, 8,14, 12,0, 1,10, 6,9,11, 5],
                [0,14, 7,11,10, 4, 13, 1, 5,8,12, 6, 9, 3, 2,15],
                [13, 8,10, 1, 3, 15, 4, 2,11, 6, 7,12, 0, 5,14, 9],
            ],
            [
                [10, 0,9,14, 6, 3,15, 5, 1,13, 12, 7,11, 4, 2,8],
                [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
                [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10,14,7],
                [1,10, 13, 0, 6, 9, 8, 7, 4,15, 14, 3, 11,5, 2,12],
            ],
            [
                [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
                [13, 8,11, 5, 6,15, 0, 3, 4,7, 2, 12, 1, 10,14,9],
                [10, 6, 9, 0, 12, 11,   7, 13,  15,  1,   3, 14,   5,  2,   8,  4],
                [3, 15,   0,  6,  10,  1,  13,  8,   9,  4,   5, 11,  12,  7,   2, 14]
            ],
            [
                [2, 12,   4,  1,   7, 10,  11,  6,   8,  5,   3, 15,  13,  0,  14,  9],
                [14, 11,   2, 12,   4,  7,  13,  1,   5,  0,  15, 10,   3,  9,   8,  6],
                [4,  2,   1, 11,  10, 13,   7,  8,  15,  9,  12,  5,   6,  3,   0, 14],
                [11,  8,  12,  7,   1, 14,   2, 13,   6, 15,   0,  9,  10,  4,   5,  3]
            ],
            [
                [12,  1,  10, 15,   9,  2,   6,  8,   0, 13,   3,  4,  14,  7,   5, 11],
                [10, 15, 4,  2,   7, 12,   9,  5,   6,  1,  13, 14,   0, 11,   3,  8],
                [9, 14,  15,  5,   2,  8,  12,  3,   7,  0,   4, 10,   1, 13,  11,  6],
                [4,  3,   2, 12,   9,  5 , 15, 10,  11, 14,   1,  7,   6,  0,   8, 13]
            ],
            [
                [4, 11,   2, 14,  15,  0,   8, 13,   3, 12,   9,  7,   5, 10,   6,  1],
                [13,  0,  11,  7,   4,  9,   1, 10,  14,  3,   5, 12,   2, 15,   8,  6],
                [1,  4,  11, 13,  12,  3,   7, 14,  10, 15,   6,  8,   0,  5,   9,  2],
                [6, 11,  13,  8,   1,  4,  10,  7,   9,  5,   0, 15,  14,  2,   3, 12],
            ],
            [
                [13,  2,   8,  4,   6, 15,  11,  1,  10,  9,   3, 14,   5,  0,  12,  7],
                [1, 15,  13,  8,  10,  3,   7,  4,  12,  5,   6, 11,   0, 14,   9,  2],
                [7, 11,   4,  1,   9, 12,  14,  2,   0,  6,  10, 13,  15,  3,   5,  8],
                [2,  1,  14,  7,   4, 10,   8, 13,  15, 12,   9,  0,   3,  5,   6, 11]
            ]
        ]

        i = self._bitlist_to_num([curr_group[0], curr_group[5]])
        j = self._bitlist_to_num(curr_group[1:5])
        return self._num_to_bitlist(s_list[index][i][j], 4)

    def _calculate_f(self, data: list, key: list) -> list:
        data_expanded = self._calculate_e(data)
        xored = self._xor_bitlist(data_expanded, key)
        s_boxed = []

        for i in range(8):
            start = i * 6
            end = start + 8
            s_boxed += self._calculate_s_box(i, xored[start:end])

        print(s_boxed)

        return xored

    def _xor_bitlist(self, l0: list, l1: list) -> list:
        size = len(l0)
        return [l0[i] ^ l1[i] for i in range(size)]

    def _encrypt_block(self, curr_block: bytearray) -> bytearray:
        curr_block_bits = [self._access_bit(curr_block, i) for i in range(64)]
        initial_permutation = self._msg_initial_permutation(curr_block_bits)

        prev_l = initial_permutation[0:32]
        prev_r = initial_permutation[32:64]

        curr_l = []
        curr_r = []

        for i in range(16):
            curr_l = prev_r
            curr_r = self._xor_bitlist(prev_l, self._calculate_f(prev_r, self._keys_48[i]))
            prev_l = curr_l
            prev_r = curr_r

        # for i in range(1, 17):
        #     li = r[i - 1]
        #     ri = self._xor_bitlist(l[i - 1], self._calculate_f(r[i - 1], self._keys_48[i - 1]))
        #     l.append(li)
        #     r.append(ri)

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
