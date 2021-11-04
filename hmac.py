import hashlib
md5_block_size = hashlib.md5().block_size
ENCODING = 'latin1'
INNER = 0
OUTER = 1

def resize_string(s):
        m = md5_block_size - len(s)
        for t in range(0,m):
                s+= chr(0)
        return s
	     
def xor_pad(key,pad):
        if pad not in [INNER, OUTER]: raise Exception('Param pad must be either INNER or OUTER')
        x = 0
        xored_bytes = []
        for c in key:
                y = (0x36 if pad == INNER else 0x5c)
                x = ord(c)^ y    
                xored_bytes.append(x)
        return xored_bytes                          


def convert_int_char(v):
        result = ""
        for l in range(0,len(v)):
                caracter = chr(v[l])
                result += caracter
        return result

def hmac_md5(key,text):
        if(len(key) < md5_block_size):
           key =  resize_string(key)
        result1 = convert_int_char(xor_pad(key,INNER))
        result2 = result1 + text
        chave1 = hashlib.md5(result2.encode(ENCODING))
        result3 = convert_int_char(xor_pad(key,OUTER))
        chave2 = hashlib.md5(result3.encode(ENCODING) + chave1.digest())
        return (chave2).digest()

def verify_hmac(key,text,expected_hash):
        return hmac_md5(key,text) == expected_hash
        

