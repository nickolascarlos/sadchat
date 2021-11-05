import hmac
import hashing
from hashaux import HashingMode, EncodingType

def generate(key: str, message: bytes) -> bytes:
    hmac_authority = hmac.HMAC(key, hashing.MD5)
    return hmac_authority.generate(message)

def verify(key: str, message: bytes, expected_hash: bytes) -> bool:
    hmac_authority = hmac.HMAC(key, hashing.MD5)
    return hmac_authority.verify(message, expected_hash)