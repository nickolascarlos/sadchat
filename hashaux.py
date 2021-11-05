import hashlib

class HashingMode:
            # RECEBE        RETORNA
    S2S = 0 # string        string
    S2B = 1 # string        byte list
    B2S = 2 # byte list     string
    B2B = 3 # byte list     byte list

class EncodingType:
    LATIN1 = 'latin1'
    ASCII  = 'ascii'
    UTF8   = 'utf8'

# Função auxiliar
def g_hash(hashfunc, data, mode, encoding):

    # Validação da consistência dos parâmetros
    if mode in [HashingMode.S2S, HashingMode.S2B] and not isinstance(data, str):
        raise Exception("Parameter 'data' must be a string when in hashing mode S2S or S2B")
    elif mode in [HashingMode.B2S, HashingMode.B2B] and not isinstance(data, bytes):
        raise Exception("Parameter 'data' must be an instance of bytes class when in hashing mode B2S or B2B")
    
    data_to_hash = data if mode in [HashingMode.B2S, HashingMode.B2B] else bytes(data, encoding)
    
    hashed = hashfunc(data_to_hash).digest()
    
    return hashed if mode in [HashingMode.S2B, HashingMode.B2B] else hashed.decode(encoding)