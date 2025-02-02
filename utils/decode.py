import base64

def decoder(b64_str: str) -> int:
    byte_data = base64.urlsafe_b64decode(b64_str)
    return int.from_bytes(byte_data, byteorder='big')