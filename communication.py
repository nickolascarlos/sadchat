import socket
import threading

import state
import strings
import hmac_bridge as hmac
from utilities import hex_format

HOST = ''
PORT = 9975

tcp = None
conn = None
client = None

friend_username = ""

def server_loop():
    global conn
    global friend_username

    try:
        while not state.get("should_threads_exit"):
            # A abertura do servidor foi movida para a função init()

            # Muda o estado para esperando
            state.update("status", "waiting")

            # Espera pela conexão
            conn, _ = tcp.accept()

            # Muda o estado para conectado
            state.update("status", "connected")

            # Faz as apresentações
            
            # Pega o nome de usuário do cliente
            friend_username = conn.recv(1024).decode('utf-8').strip()

            # Verifica se os usernames são iguais
            # Se forem, corta a conexão
            if (friend_username == state.get_username()):
                conn.sendall(bytes(strings.same_usernames_not_allowed, 'utf-8'))
                state.add_message("command", strings.same_usernames_not_allowed)
                conn.sendall(bytes('bye', 'utf-8'))
                conn.close()
                conn = None
                state.update("status", "waiting")
                continue
            
            state.add_message("command", strings.connected_to % (str(friend_username)))

            # Envia seu nome pro cliente
            conn.sendall(bytes(state.get("username"), "utf-8"))

            messages_loop()

    except Exception as e:
        state.add_message("command", "[!] SVR: " + str(e))

def connect_to_server(host, port):
    global conn
    global tcp
    global friend_username
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp.settimeout(5) # Define 5s de timeout
        tcp.connect((host, port))
        tcp.settimeout(None) # Como eu quero timeout só pra conexão, aqui eu tiro
                          # para não afetar a comunicação
        conn = tcp
    except Exception as e:
        state.add_message("command", strings.connection_couldnt_be_established)
        tcp = None
        return
        
    state.update("status", "connected")

    # Envia seu nome pro servidor
    conn.sendall(bytes(state.get("username"), "utf-8"))

    # Pega o nome de usuário do servidor
    friend_username = conn.recv(1024).decode('utf-8').strip()
    state.add_message("command", strings.connected_to % (str(friend_username)))

    messages_loop()

def messages_loop():
    global conn
    global friend_username

    try:
        while not state.get("should_threads_exit"):
            received = conn.recv(1024)

            message: bytes = received[0:-16]
            expected_hash: bytes = received[-16:]

            # state.add_message(friend_username, str(list(received)))

            message_str: str = message.decode('latin1')

            if message_str.strip() == 'bye' or not message_str:
                conn.close()
                conn = None
                state.add_message("command", strings.friend_disconnected % (friend_username))
                state.update("status", "offline")
                break

            # Verifica se a mensagem é válida
            valid = hmac.verify(state.get("secret"), message, expected_hash)

            state.add_message(friend_username, message_str, valid)
            
            if not valid:
                calculated_hash = hmac.generate(state.get("secret"), message) # Calcula o HMAC para mostrar para o usuário
                state.add_message("command", strings.invalid_message % (hex_format(expected_hash.hex()), hex_format(calculated_hash.hex())))


    except Exception as e:
        state.add_message("command", str(e))

def send_message(message):
    global conn

    if not conn:
        state.add_message("command", strings.please_connect_before_sending_messages)
        return

    try:
        message_bytes = bytes(message, 'latin1')
        hmac_hash = hmac.generate(state.get("secret"), message_bytes)
    except Exception as e:
        state.add_message("command", str(e))

    # Envia a mensagem para o contato
    conn.sendall(message_bytes + hmac_hash)

    # Adiciona a mensagem à lista
    state.add_message(state.get_username(), message)
    
def init():
    global tcp

    # Abre o servidor
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        tcp.bind((HOST, state.get("port")))
        tcp.listen(1)
    except Exception as e:
        state.add_message("command", "Error: " + str(e)[0:150]+'...')
        tcp = None
        return -1, -1

    y = threading.Thread(target = server_loop)
    y.name = "Communication-SERVER-THREAD"
    y.start()

    return HOST, state.get("port")        

def connect_to(host, port):
    y = threading.Thread(target = connect_to_server, args=(host, int(port) if port else 9975))
    y.name = "Communication-CLIENT-THREAD"
    y.start()

# Função para verificar se o usuário
# está apto a realizar uma conexão; isso é:
# Se ele já tem um usuário e já definiu uma chave
# para o HMAC
def is_able_to_connect(verbose = False):
    is_able = state.get_username() != '' and state.get("secret") != ''
    if not is_able and verbose:
        state.add_message("command", strings.please_set_user_and_secret)
    return is_able