import buffer

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
    command_args = tokenized_command[1:]

    # Como Python não tem switch...
    try:
        ({
            'buffer': exec_buffer,
            'echo': exec_echo
        })[tokenized_command[0][1:]](command_args)
    except Exception as e:
        # Se não houver nenhum comando com o nome especificado
        print('No command!')

#  -------------------------------
# |   Implementação dos Comandos  |
#  -------------------------------

def exec_buffer(args):
    print(buffer.buffer)

def exec_echo(args):
    print("\n\n%s\n" % (args[0]))
