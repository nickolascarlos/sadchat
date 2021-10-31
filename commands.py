import buffer
import strings
from strings import __
import state
import communication

def tokenize_command(command):
    args = command.split(" ")
    processed_args = []
    quote_flag = False
    for arg in args:

        if quote_flag:
            processed_args[-1] += " " + arg
        else:
            processed_args.append(arg)

        if arg.startswith("\""):
            quote_flag = True
        if arg.endswith("\""):
            quote_flag = False
    
    for i in range(0, len(processed_args)):
        arg = processed_args[i]

        if arg.startswith("\"") and arg.endswith("\""):
            processed_args[i] = arg[1:][:-1]

    return processed_args

def process_command(command):
    
    tokenized_command = tokenize_command(command)

    # Argumentos para o comando: todos os elementos tokenizados,
    # menos o primeiro, que se trata justamente do comando
    command_args = tokenized_command[1:] if len(tokenized_command) > 1 else []

    # Como Python não tem switch...
    try:
        ({
            'buffer': exec_buffer,
            'echo': exec_echo,
            'ss': exec_ss,
            'whoami': exec_whoami,
            'setuser': exec_setuser,
            'start': exec_start,
            'conn': exec_conn,
            'chkconn': exec_chkconn
        })[tokenized_command[0][1:]](command_args)
    except Exception as e:
        # Se não houver nenhum comando com o nome especificado
        state.add_message("command", "Unknown command ::" + str(e))


#  -------------------------------
# |   Implementação dos Comandos  |
#  -------------------------------

def exec_buffer(args):
    print(buffer.buffer)

def exec_echo(args):
    state.add_message("command", args[0])

def exec_ss(args):
    secret = args[0] if len(args) > 0 else ""
    if secret:
        state.update("secret", args[0])
        state.add_message("command", strings.secret_set)
    else:
        state.add_message("command", strings.your_secret_is % (configs.get_secret()))

def exec_whoami(_):
    # state.add_message("command", strings.please_set_your_username)
    username = state.get("username")
    if (username):
        state.add_message("command", strings.your_username_is % (username))
    else:
        state.add_message("command", strings.please_set_your_username)

def exec_setuser(args):
    if (len(args) < 1):
        return state.add_message("command", strings.insufficient_arguments)
    if (args[0].strip() in ['', 'command']):
        return state.add_message("command", strings.forbidden_username)

    state.set_username(args[0].strip())
    state.add_message("command", strings.username_set % (args[0].strip()))

def exec_start(_):
    # Se o servidor já estiver aberto, avisa
    if communication.tcp: return state.add_message("command", "Servidor já aberto e aguardando conexão")
    
    _host, _port = communication.init() 
    state.add_message("command", strings.waiting_for_connection % (_host, _port))

def exec_conn(args):
    if (len(args) < 1):
        return state.add_message("command", strings.insufficient_arguments)

    host = args[0]
    port = args[1] if len(args) > 1 else None
    state.add_message("command", strings.connecting_to % (host, port))
    communication.connect_to(host, port)

def exec_chkconn(args):
    return # TODO
    if (len(args) < 1):
        return state.add_message("command", strings.insufficient_arguments)

    host = args[0]
    port = args[1] if len(args) > 1 else None

    state.add_message("command", strings.connecting_to % (host, port))
    communication.conn(host, port)
