
# Formata uma string HEX separando com um espaço de dois em dois caracteres
# e capitalizando as letras
def hex_format(s: str) -> str:
    return ' '.join(s[i*2:(i+1)*2] for i in range(0, len(s)//2)).upper()