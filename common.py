import random
import base64
from hashlib import sha256


SERVER_SERVICE_PORT = 50000
AUTH_SERVER_PORT = 50001
TICKET_GRANTING_SERVER_PORT = 50002
CLIENT_PORT = 50003

MAX_DATA_LEN = 1024


def delete_trailing_zeros(data: bytes) -> bytes:
    return data.rstrip(bytes('\x00', 'utf-8'))


def sha256hash(string: str) -> bytes:
    return sha256(string.encode("utf-8")).digest()


def gen_key() -> bytes:
    key = random.randint(0, 9223372036854775807)
    return key.to_bytes(8, "big")


def bytes_to_string(b: bytes) -> str:
    return base64.b64encode(b).decode("ascii")


def string_to_bytes(s: str) -> bytes:
    return base64.b64decode(s)
