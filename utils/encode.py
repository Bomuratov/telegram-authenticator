import base64
import os

def encoder(n: int) -> str:
    salt = os.urandom(2)
    byte_data = salt + n.to_bytes((n.bit_length() + 7) // 8, byteorder='big')
    return base64.urlsafe_b64encode(byte_data).decode()
