# Módulo para o buffer do teclado

buffer = ""

def get_buffer():
    global buffer
    return buffer

def clear_buffer():
    global buffer
    buffer = ""

# Função para 'corrigir' o buffer, substituindo sequências como
# "~a", "~o", "`a", etc. para "ã", "õ", "à"
def process_buffer():
    global buffer
    equivalences = [

                    ["~a", "ã"],
                    ["´a", "á"],
                    ["`a", "ã"],
                    ["^a", "â"],
                    ["¨a", "ä"],

                    ["~A", "Ã"],
                    ["´A", "Á"],
                    ["`A", "À"],
                    ["^A", "Â"],
                    ["¨A", "Ä"],

                    ["~e", "ẽ"],
                    ["´e", "é"],
                    ["`e", "è"],
                    ["^e", "ê"],
                    ["¨e", "ë"],

                    ["~E", "Ẽ"],
                    ["´E", "É"],
                    ["`E", "È"],
                    ["^E", "Ê"],
                    ["¨E", "Ë"],

                    ["~i", "ĩ"],
                    ["´i", "í"],
                    ["`i", "ì"],
                    ["^i", "î"],
                    ["¨i", "ï"],

                    ["~I", "Ĩ"],
                    ["´I", "Í"],
                    ["`I", "Ì"],
                    ["^I", "Î"],
                    ["¨I", "Ï"],

                    ["~o", "õ"],
                    ["´o", "ó"],
                    ["`o", "ò"],
                    ["^o", "ô"],
                    ["¨o", "ö"],

                    ["~O", "Õ"],
                    ["´O", "Ó"],
                    ["`O", "Ò"],
                    ["^O", "Ô"],
                    ["¨O", "Ö"],

                    ["~u", "ũ"],
                    ["´u", "ú"],
                    ["`u", "Ù"],
                    ["^u", "û"],
                    ["¨u", "ü"],

                    ["~U", "Ũ"],
                    ["´U", "Ú"],
                    ["`U", "Ù"],
                    ["^U", "Û"],
                    ["¨U", "Ü"]
                    
                ]
    # processed_buffer = buffer
    for equivalence in equivalences:
        buffer = buffer.replace(equivalence[0], equivalence[1])
    
    # return processed_buffer