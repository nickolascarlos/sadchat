import curses
from curses import wrapper
import time
import random
from random import randint
import math
import threading

import buffer
import asciiart
import strings

import state

stdscr = None

def init_screen():
    global stdscr

    stdscr = curses.initscr()
    curses.echo(False)

    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(5, curses.COLOR_RED, -1)
    curses.init_pair(6, curses.COLOR_GREEN, -1)
    curses.init_pair(7, curses.COLOR_YELLOW, -1)
    curses.init_pair(8, curses.COLOR_MAGENTA, -1)
    curses.init_pair(9, curses.COLOR_BLUE, -1)
    curses.init_pair(10, curses.COLOR_BLACK, curses.COLOR_BLUE)
    curses.init_pair(11, curses.COLOR_GREEN, curses.COLOR_BLUE)
    curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    # draw_initial_screen()

def draw_image(image, x, y, text_attrs):
    # x = -1 e y = -1 para centralizar imagem
    global stdscr

    height, width = stdscr.getmaxyx()

    image_height = len(image)
    image_width = len(image[0])

    image_y_start_centered = (height//2) - (image_height//2)
    image_x_start_centered = (width//2) - (image_width//2)

    for _y in range(0, image_height):
        for _x in range(0,image_width):
            stdscr.addstr((image_y_start_centered if y == -1 else y) + _y, (image_x_start_centered if x == -1 else x) + _x, image[_y][_x], text_attrs)

    stdscr.move(0, 0)

def draw_initial_screen():
    global stdscr

    height, width = stdscr.getmaxyx()

    stdscr.clear()
    stdscr.refresh()

    face_height = len(asciiart.happy_face)
    face_width = len(asciiart.happy_face[0])

    face_y_start_centered = (height//2) - (face_height//2)
    face_x_start_centered = (width//2) - (face_width//2)

    faces = [asciiart.happy_face, asciiart.sad_face]

    for k, face in enumerate(faces):
        stdscr.clear()
        
        draw_image(face, -1, -1, curses.color_pair(0))

        time.sleep(0.8)
        stdscr.refresh()
    
    time.sleep(0.8)
    stdscr.clear()
        
    draw_image(asciiart.sad_text, -1, -1, curses.color_pair(0))

    stdscr.refresh()
    time.sleep(1.5)
    

def draw_interface():
    global stdscr

    height, width = stdscr.getmaxyx()

    stdscr.clear()
    # Desenha a barra superior
    for i in range(0, width):
        for j in range(0, 3):
            stdscr.addstr(j, i, " ", curses.color_pair(1))    

    # Escreve alerta 1
    stdscr.addstr(1, 3, state.get("main_alert"), curses.color_pair(1))

    # Escreve estado da conexão
    conn_status = state.get("status")
    stdscr.addstr(1, width - len(conn_status) - 3, conn_status, curses.A_BOLD | curses.color_pair(11 if conn_status == 'connected' else (12 if conn_status == 'waiting' else 10)))

    # Desenha a caixa de texto (barra inferior)
    for i in range(0, width):
        for j in range(0, 3):
            stdscr.addstr(height-4-j, i, " ", curses.color_pair(3))
    
    # Não imprime os caracteres em excesso
    stdscr.addstr(height-3, 0, " > " + state.get("buffer")[0:width-4], curses.color_pair(0))

    # Escreve o estado do segredo
    if not state.get("secret"):
        stdscr.addstr(height-5, 15, "[!] " + strings.secret_not_set, curses.color_pair(4))

    draw_messages()

    # Escreve a hora
    draw_hour(False)

    # Finalmente
    fix_cursor()
    stdscr.refresh()

def draw_hour(call_rerender=True):
    global stdscr

    height, width = stdscr.getmaxyx()

    # Escreve a hora
    stdscr.addstr(height-5, 3, state.get("time"), curses.color_pair(3))

    if (call_rerender):
        rerender()

    # Finalmente
    fix_cursor()
    stdscr.refresh()

# TODO: Excluir ou modificar. Ineficiente
def check_if_messages_fit_the_screen(quantity):
    global stdscr

    height, width = stdscr.getmaxyx()

    # %Quantity% partindo da última mensagem
    
    # Últimas %quantity% mensagens
    messages = state.get("messages")
    last_q_messages = messages[-quantity:]

    # Faremos uma simulação da impressão das mensagens
    # Se line_to_write, ao final, for maior que height - 7, então as últimas %quantity% mensagens
    # não cabem na tela
    line_to_write = 4 # Linha inicial = 4
    for message in last_q_messages:
        sender = message[1]
        offset = width - 15 - len(sender)
        line_to_write += 1
        for i in range(0, math.ceil(len(message[2][offset:]) / width)):
            line_to_write += 1

    if (line_to_write > height - 6):
        return False
    return True

def draw_messages():
    global stdscr
    
    height, width = stdscr.getmaxyx()

    # Quantidade de mensagens a se imprimir (a contar da última)
    # TODO: Melhorar. Método ineficiente
    quantity_messages_to_print = 30 # Não imprime mais que 30 mensagens, por uma questão de eficiência
    while (not check_if_messages_fit_the_screen(quantity_messages_to_print)):
        quantity_messages_to_print -= 1
    
    messages = state.get("messages")
    messages_to_print = messages[-quantity_messages_to_print:] # Pega as %n% últimas mensagens

    # Escreve as mensagens
    line_to_write = 3 # Linha inicial = 4
    for message in messages_to_print:
        # Imprimimos a hora
        stdscr.addstr(line_to_write, 1, message[0], curses.color_pair(7))
        
        sender = message[1]

        if (sender != "command"): # TODO: Melhorar
            # Imprimimos o remetente
            stdscr.addstr(line_to_write, 12, sender,  curses.A_BOLD | (curses.color_pair(9) if sender == state.get_username() else curses.color_pair(8)))

            # Imprimimos o indicador de verificação HMAC
            verified = message[3]
            stdscr.addstr(line_to_write, 12 + len(sender), " [%s] " % ("👍" if verified else "❌"), curses.A_BOLD | curses.color_pair(8))

            offset = width - 15 - len(sender)
            # Imprimimos a primeira linha da mensagem:
            stdscr.addstr(line_to_write, 19 + len(sender), message[2][0:offset], curses.color_pair(0))
            line_to_write += 1
            # Imprime o resto da mensagem
            for i in range(0, math.ceil(len(message[2][offset:]) / width)):
                message_l = message[2][offset + (width * i): offset + (width * (i+1))]
                # if (not message_l): break
                stdscr.addstr(line_to_write, 0, message_l, curses.color_pair(0))
                line_to_write += 1
        else:
            offset = width - 12
            # Imprimimos a primeira linha da mensagem:
            stdscr.addstr(line_to_write, 12, message[2][0:offset], curses.A_BOLD | curses.color_pair(5))
            line_to_write += 1
            # Imprime o resto da mensagem
            for i in range(0, math.ceil(len(message[2][offset:]) / width)):
                message_l = message[2][offset + (width * i): offset + (width * (i+1))]
                # if (not message_l): break
                stdscr.addstr(line_to_write, 0, message_l, curses.A_BOLD | curses.color_pair(5))
                line_to_write += 1
    
    fix_cursor()
    stdscr.refresh()

def fix_cursor():
    global stdscr
    # Coloca o cursor no seu devido lugar

    height, width = stdscr.getmaxyx()

    current_cursor_position = state.get("cursor_position")
    stdscr.move(height-3, (current_cursor_position + 3) if (current_cursor_position + 3 < width) else (width - 1))

def draw_gui():
    global stdscr

    stdscr.clear()
    stdscr.refresh()

    draw_interface()

# Função para re-renderizar a interface de usuário
def rerender():
    draw_gui()    

init_screen()

# Inicia a thread que desenhará a interface
y = threading.Thread(target=draw_gui)
y.start()
