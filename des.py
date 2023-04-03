from bitarray import bitarray


class Des:
    def __init__(self, plain_message: str, key: bytearray):
        self._plain_data = bytearray(plain_message, "utf-8")
        self._key = key
        # print(key.hex())
        self._encrypted_data = bytearray()

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