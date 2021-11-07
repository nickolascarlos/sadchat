import buffer
import strings
import state
import communication

# Histórico dos comandos executados
commands_history = []

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

    add_command_to_history(command)

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
            'su': exec_su,
            'start': exec_start,
            'conn': exec_conn,
            'chkconn': exec_chkconn
        })[tokenized_command[0][1:]](command_args)
    except Exception as e:
        # Se não houver nenhum comando com o nome especificado
        state.add_message("command", "Unknown command ::" + str(e))

def add_command_to_history(command, refreshIndex = True):
    global commands_history

    commands_history.append(command)

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

        state.update("main_alert", strings.to_see_your_secret)

        if state.get_username():
            state.add_message("command", strings.all_set)

    else:
        state.add_message("command", strings.your_secret_is % (state.get("secret")))

def exec_whoami(_):
    username = state.get("username")
    state.add_message("command", (strings.your_username_is % (username)) if username else strings.please_set_your_username)

def exec_su(args):
    if (len(args) < 1):
        return state.add_message("command", strings.insufficient_arguments)
    if (args[0].strip() in ['', 'command']):
        return state.add_message("command", strings.forbidden_username)

    state.set_username(args[0].strip())
    state.add_message("command", strings.username_set % (args[0].strip()))

    if not state.get("secret"):
        state.update("main_alert", strings.set_your_secret)
    else:
        state.add_message("command", strings.all_set)


def exec_start(_):

    if not communication.is_able_to_connect(verbose = True): return

    # Se o servidor já estiver aberto, avisa
    if communication.tcp: return state.add_message("command", strings.server_waiting_for_connection)
    
    _host, _port = communication.init() 
    state.add_message("command", strings.waiting_for_connection % (_host, _port))

def exec_conn(args):
    if not communication.is_able_to_connect(verbose = True): return

    if len(args) < 1:
        return state.add_message("command", strings.insufficient_arguments)

    host = args[0]
    port = args[1] if len(args) > 1 else None
    state.add_message("command", strings.connecting_to % (host, port))
    communication.connect_to(host, port)

def exec_chkconn(_):
    state.add_message("command", (strings.you_are_connected_to % (communication.friend_username)) if communication.conn else (strings.your_are_disconnected))
