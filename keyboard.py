from datetime import datetime
import threading

from commands import *
import buffer
import state
import gui
from communication import send_message

commands_history_access_index = 0

def watch_keys():
    global commands_history_access_index

    while True:
        try:
            p_key_pressed = gui.stdscr.get_wch()
            key_pressed = ord(p_key_pressed)

            if key_pressed == 10: # Enter
                # Verifica se o que está no buffer se trata de um comando
                # Se for, o processa
                # Do contrário, assume-se ser uma mensagem
                if  buffer.get_buffer().startswith("!"):
                    process_command(buffer.get_buffer())
                    commands_history_access_index = 0
                else:
                    if buffer.get_buffer(): # EVita o processamento de buffer vazio
                        send_message(buffer.get_buffer())
                # E então limpa o buffer
                buffer.clear_buffer()
            elif key_pressed == 127: # Backspace
                buffer.backspace()
            elif (32 <= key_pressed <= 126 or 192 <= key_pressed <= 255): # Caractere normal
                buffer.append(chr(key_pressed))
            elif key_pressed == 27:
                # Tecla especial (como setas)

                # Lê as próximas duas para determinar qual foi a tecla pressionada
                cod_0 = ord(gui.stdscr.get_wch())
                cod_1 = ord(gui.stdscr.get_wch())

                if cod_0 == 91:
                    # Setas
                    if cod_1 == 65: # Cima
                        # Navega no histórico de comandos
                        if commands_history_access_index > -1 * len(commands_history):
                            commands_history_access_index -= 1
                        buffer.set_buffer(commands_history[commands_history_access_index])
                        state.set_cursor_position_to_left_end()
                    elif cod_1 == 66: # Baixo
                        # Navega no histórico de comandos
                        if commands_history_access_index < len(commands_history)-1:
                            commands_history_access_index += 1
                        buffer.set_buffer(commands_history[commands_history_access_index])
                        state.set_cursor_position_to_left_end()
                    elif cod_1 == 67:
                        state.inc_cursor_position()
                    elif cod_1 == 68:
                        state.dec_cursor_position()

                
        except Exception:
            pass


def start_keyboard_listening():
    y = threading.Thread(target=watch_keys)
    y.name = "Keyboard-THREAD"
    y.start()