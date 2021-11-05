from typing import Union
from hashaux import g_hash, HashingMode, EncodingType
import hashlib



def MD5(data: Union[str, bytes], mode: HashingMode, encoding: EncodingType = EncodingType.LATIN1):
    return g_hash(hashlib.md5, data, mode, encoding)

def SHA256(data: Union[str, bytes], mode: HashingMode, encoding: EncodingType = EncodingType.LATIN1):
    return g_hash(hashlib.sha256, data, mode, encoding)

def SHA1(data: Union[str, bytes], mode: HashingMode, encoding: EncodingType = EncodingType.LATIN1):
    return g_hash(hashlib.sha1, data, mode, encoding)