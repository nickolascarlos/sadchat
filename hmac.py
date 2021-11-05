# Algoritmo escrito de acordo com <https://cseweb.ucsd.edu//~mihir/papers/hmac-cb.pdf>

import hashlib
from typing import Callable, Union

from hashaux import HashingMode, EncodingType

ENCODING = EncodingType.LATIN1 # Usado na conversão string -> bytes

INNER = 1
OUTER = 2

class HMAC:

    def __init__(self, K: str, H: Callable):
        self.key = HMAC.resize_key(K)
        self.hashfunc = H

    # Função para a geração do HMAC de uma mensagem
    # Parâmetros:
    #   K = chave
    #   Text = mensagem
    #   H = função de hashing
    def generate(self, Text: Union[str, bytes]) -> bytes:
        if type(Text) == str:
            Text: bytes = bytes(Text, ENCODING) # Converte a mensagem em bytes        
        inner_hash: bytes = self.hashfunc(HMAC.xor_key(INNER, self.key) + Text, HashingMode.B2B, EncodingType.LATIN1)
        return self.hashfunc(HMAC.xor_key(OUTER, self.key) + inner_hash, HashingMode.B2B, EncodingType.LATIN1)

    # Verifica a integridade e autenticidade de uma mensagem
    def verify(self, Text: str, expected_hash: bytes) -> bool:
        return self.generate(Text) == expected_hash

    # Gera um "pacote" de bytes contendo a mensagem e sua hash, separadas por um byte 0x00:
    # bytes(mensagem) || 0x00 || bytes(hash)
    def generate_pack(self, Text: str) -> bytes:
        encoded_text = bytes(Text, ENCODING)
        message_hash = self.generate(Text)
        return encoded_text + bytes([0]) + message_hash
    
    # Verifica o "pacote" formado pela mensagem e pela hash
    def verify_pack(self, pack: bytes) -> bool:
        Text, expected_hash = pack.split(b'\x00')
        return self.generate(Text) == expected_hash

    # Retorna key acrescida de quantos 0's forem necessários
    # para se completarem 64 caracteres, conforme especificado
    # no artigo (no topo desse arquivo) em que esse trabalho se baseia
    @staticmethod
    def resize_key(key: str) -> str:
        # O artigo em que esse script foi baseado não define uma abordagem
        # clara para quando a chave tiver mais de 64 caracteres
        if len(key) > 64: raise Exception('key size must be less or equal to 64')
        number_of_zeros_to_append = 64 - len(key)
        return bytes(key, ENCODING) + bytes([0]) * number_of_zeros_to_append

    # Função para realizar o xor entre a chave e (ipad ou opad)
    # Parâmetros:
    #   w = INNER | OUTER
    #   key = chave
    @staticmethod
    def xor_key(w: int, key: bytes) -> bytes:
        base = 0x36 if w == INNER else (0x5C if w == OUTER else None)
        if not base: raise ValueError('Parameter w must be either INNER or OUTER')
        xored_key = []
        for byte in key:
            xored_key.append(byte ^ base)
        return bytes(xored_key)