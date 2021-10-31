from datetime import datetime
import threading

from commands import *
import buffer
import state
import gui
from communication import send_message

def watch_keys():
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
                else:
                    send_message(buffer.get_buffer())
                # E então limpa o buffer
                buffer.clear_buffer()
            elif key_pressed == 127: # Backspace
                buffer.backspace()
            elif (32 <= key_pressed <= 126 or 192 <= key_pressed <= 255): # Caractere normal
                buffer.append(chr(key_pressed))
        except Exception:
            pass
        # # if key_pressed == curses.KEY_ENTER:
        # state.add_message("quiiboah", str(key_pressed))


def start_keyboard_listening():
    y = threading.Thread(target=watch_keys)
    y.name = "Keyboard-THREAD"
    y.start()